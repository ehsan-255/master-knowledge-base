# Vault Configuration for Scribe HMA v2.2
# Production-ready configuration for HashiCorp Vault

# Storage backend (file system for development)
storage "file" {
  path = "/vault/data"
}

# HTTP listener
listener "tcp" {
  address         = "0.0.0.0:8200"
  cluster_address = "0.0.0.0:8201"
  tls_disable     = 1
}

# API address
api_addr = "http://0.0.0.0:8200"
cluster_addr = "http://0.0.0.0:8201"

# UI access
ui = true

# Disable memory locking for development
disable_mlock = true

# Logging
log_level = "INFO"
log_format = "json"

# Telemetry for observability integration
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname = true
}

# Plugin directory
plugin_directory = "/vault/plugins"

# Default lease TTL and max lease TTL
default_lease_ttl = "168h"
max_lease_ttl = "720h"

# Seal configuration (for production, use auto-unseal)
# seal "transit" {
#   address = "https://vault.company.com:8200"
#   key_name = "autounseal"
#   mount_path = "transit/"
# }

# Entropy augmentation (for production)
# entropy "seal" {
#   mode = "augmentation"
# }