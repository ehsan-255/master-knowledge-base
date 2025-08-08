# Vault Setup for Scribe (Development)

## Prerequisites
- Vault server reachable from the cluster or local environment.
- Kubernetes auth method enabled on Vault.

## Enable KV and Kubernetes auth
vault secrets enable -path=kv kv
vault auth enable kubernetes

## Configure Kubernetes auth (example for default namespace)
vault write auth/kubernetes/config \
  token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token \
  kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

## Policy for read-only access
cat > scribe-readonly.hcl <<'EOF'
path "kv/data/scribe/*" {
  capabilities = ["read"]
}
EOF
vault policy write scribe-readonly scribe-readonly.hcl

## Role binding service account scribe-sa to policy
vault write auth/kubernetes/role/scribe-role \
  bound_service_account_names=scribe-sa \
  bound_service_account_namespaces=default \
  policies=scribe-readonly \
  ttl=24h

## Provision development secrets
vault kv put kv/scribe/nats url="nats://nats:4222" creds="user:pass"
vault kv put kv/scribe/tls server.crt="$(cat tools/reports/server.crt)" server.key="$(cat tools/reports/server.key)" ca.crt="$(cat tools/reports/ca.crt)"