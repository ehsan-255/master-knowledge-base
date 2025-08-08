#!/bin/bash
set -e

echo "🔐 Initializing Vault for Scribe HMA v2.2 Secrets Management..."

# Wait for Vault to be ready
echo "⏳ Waiting for Vault server to be ready..."
until vault status > /dev/null 2>&1; do
    echo "Waiting for Vault..."
    sleep 2
done

echo "✅ Vault server is ready"

# Enable KV v2 secrets engine for application secrets
echo "🔧 Enabling KV v2 secrets engine..."
vault secrets enable -path=scribe kv-v2 || echo "KV v2 engine already enabled"

# Enable PKI secrets engine for certificate management
echo "🔧 Enabling PKI secrets engine..."
vault secrets enable -path=pki pki || echo "PKI engine already enabled"

# Configure PKI engine
echo "🔧 Configuring PKI certificate authority..."
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA certificate
vault write -field=certificate pki/root/generate/internal \
    common_name="Scribe HMA v2.2 Root CA" \
    ttl=87600h > /tmp/scribe-ca.crt

# Configure PKI URLs
vault write pki/config/urls \
    issuing_certificates="http://vault:8200/v1/pki/ca" \
    crl_distribution_points="http://vault:8200/v1/pki/crl"

# Create PKI role for Scribe services
echo "🔧 Creating PKI role for Scribe services..."
vault write pki/roles/scribe-role \
    allowed_domains="scribe.local,localhost" \
    allow_subdomains=true \
    max_ttl="8760h" \
    generate_lease=true

# Enable AppRole auth method for service authentication
echo "🔧 Enabling AppRole authentication..."
vault auth enable approle || echo "AppRole auth already enabled"

# Create comprehensive policy system for production deployment
echo "📋 Creating enterprise Vault policies..."

# Admin Policy - Full administrative access
vault policy write scribe-admin - <<EOF
# Full administrative access for Scribe administrators
# Default TTL: unlimited
# Max TTL: unlimited

path "*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "sys/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}

path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
EOF

# Service Policy - Service-level operations
vault policy write scribe-service - <<EOF
# Service-level access for Scribe engine operations
# Default TTL: 1h
# Max TTL: 4h

path "scribe/data/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "scribe/metadata/*" {
  capabilities = ["list", "read", "delete"]
}

path "pki/issue/scribe-role" {
  capabilities = ["create", "update"]
}

path "pki/certs" {
  capabilities = ["list"]
}

path "pki/revoke" {
  capabilities = ["create", "update"]
}

path "sys/health" {
  capabilities = ["read", "sudo"]
}

path "sys/capabilities-self" {
  capabilities = ["read"]
}
EOF

# Application Policy - Application-specific access
vault policy write scribe-application - <<EOF
# Application-specific access for Scribe components
# Default TTL: 30m
# Max TTL: 2h

path "scribe/data/config/*" {
  capabilities = ["read"]
}

path "scribe/data/secrets/application/*" {
  capabilities = ["read"]
}

path "pki/issue/scribe-role" {
  capabilities = ["create", "update"]
}

path "sys/health" {
  capabilities = ["read"]
}
EOF

# Read-Only Policy - Monitoring and auditing
vault policy write scribe-readonly - <<EOF
# Read-only access for monitoring and auditing
# Default TTL: 2h
# Max TTL: 8h

path "scribe/data/*" {
  capabilities = ["read", "list"]
}

path "scribe/metadata/*" {
  capabilities = ["read", "list"]
}

path "sys/health" {
  capabilities = ["read"]
}

path "sys/capabilities-self" {
  capabilities = ["read"]
}
EOF

# Emergency Policy - Time-limited emergency access
vault policy write scribe-emergency - <<EOF
# Emergency access with time and usage limits
# Default TTL: 15m
# Max TTL: 1h

path "scribe/data/emergency/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "pki/issue/scribe-role" {
  capabilities = ["create", "update"]
}

path "sys/health" {
  capabilities = ["read", "sudo"]
}
EOF

echo "🔐 Creating production AppRoles..."

# Scribe Engine AppRole - Primary service authentication
vault write auth/approle/role/scribe-engine \
    token_policies="scribe-service" \
    token_ttl="1h" \
    token_max_ttl="4h" \
    token_no_default_policy=true \
    secret_id_ttl="10m" \
    secret_id_num_uses=1 \
    bind_secret_id=true \
    local_secret_ids=false

# Application AppRole - Application component authentication
vault write auth/approle/role/scribe-application \
    token_policies="scribe-application" \
    token_ttl="30m" \
    token_max_ttl="2h" \
    token_no_default_policy=true \
    secret_id_ttl="5m" \
    secret_id_num_uses=1 \
    bind_secret_id=true

# Monitoring AppRole - Read-only monitoring access
vault write auth/approle/role/scribe-monitoring \
    token_policies="scribe-readonly" \
    token_ttl="2h" \
    token_max_ttl="8h" \
    token_no_default_policy=true \
    secret_id_ttl="15m" \
    secret_id_num_uses=3 \
    bind_secret_id=true

# Emergency AppRole - Emergency access with restrictions
vault write auth/approle/role/scribe-emergency \
    token_policies="scribe-emergency" \
    token_ttl="15m" \
    token_max_ttl="1h" \
    token_no_default_policy=true \
    secret_id_ttl="2m" \
    secret_id_num_uses=1 \
    bind_secret_id=true

# Get role-id and secret-id for the engine
ROLE_ID=$(vault read -field=role_id auth/approle/role/scribe-engine/role-id)
SECRET_ID=$(vault write -field=secret_id -f auth/approle/role/scribe-engine/secret-id)

echo "📝 AppRole credentials:"
echo "Role ID: $ROLE_ID"
echo "Secret ID: $SECRET_ID"

# Store initial secrets for demonstration
echo "💾 Storing initial secrets..."

# Store mTLS certificates in Vault
vault kv put scribe/certificates/mtls \
    ca_cert="$(cat /vault/config/ca.crt 2>/dev/null || echo 'placeholder-ca-cert')" \
    server_cert="$(cat /vault/config/server.crt 2>/dev/null || echo 'placeholder-server-cert')" \
    server_key="$(cat /vault/config/server.key 2>/dev/null || echo 'placeholder-server-key')"

# Store application configuration secrets
vault kv put scribe/config/application \
    database_password="secure-db-password-123" \
    api_key="scribe-api-key-456" \
    encryption_key="$(openssl rand -base64 32)"

# Store NATS configuration
vault kv put scribe/config/nats \
    username="scribe_user" \
    password="$(openssl rand -base64 24)" \
    cluster_secret="$(openssl rand -base64 32)"

# Store observability configuration
vault kv put scribe/config/observability \
    prometheus_password="$(openssl rand -base64 16)" \
    grafana_admin_password="$(openssl rand -base64 16)" \
    jaeger_secret="$(openssl rand -base64 24)"

echo "✅ Vault initialization completed successfully!"
echo "🔐 Vault is configured with:"
echo "   - KV v2 secrets engine at 'scribe/'"
echo "   - PKI secrets engine for certificate management"
echo "   - AppRole authentication for services"
echo "   - Security policies for Scribe engine"
echo "   - Initial secrets for demonstration"

# Display vault status
echo "📊 Vault Status:"
vault status