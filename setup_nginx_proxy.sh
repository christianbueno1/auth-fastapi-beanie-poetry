#!/bin/bash
# filepath: /home/chris/projects/auth-fastapi-beanie-poetry/setup_nginx_proxy.sh

set -e  # Exit on any error

# Variables
# DOMAIN_NAME="localhost"
ROOT_DOMAIN="christianbueno.tech"
SUBDOMAIN="authapi"
FULL_DOMAIN_NAME="$SUBDOMAIN.$ROOT_DOMAIN" # or use localhost
NGINX_CONFIG="/etc/nginx/conf.d/$FULL_DOMAIN_NAME.conf"
NGINX_LOG_DIR="/var/log/nginx"
NGINX_LOG_FILE="$NGINX_LOG_DIR/authapi-access.log"
NGINX_ERROR_LOG_FILE="$NGINX_LOG_DIR/authapi-error.log"

# Function to handle errors
handle_error() {
    echo "❌ ERROR: $1"
    exit 1
}

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
  echo "🚨 Please run this script with sudo"
  exit 1
fi

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    echo "📦 Installing Nginx..."
    dnf install -y nginx || handle_error "Failed to install Nginx"
    echo "✅ Nginx installed successfully"
else
    echo "✅ Nginx already installed"
fi

# Create Nginx configuration
echo "✏️  Creating Nginx proxy configuration..."
cat > $NGINX_CONFIG << EOF
server {
    listen 80;
    server_name localhost $FULL_DOMAIN_NAME;

    # Access log and error log
    access_log $NGINX_LOG_FILE;
    error_log $NGINX_ERROR_LOG_FILE;

    # Proxy for API
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # # WebSocket support (if needed)
        # proxy_http_version 1.1;
        # proxy_set_header Upgrade \$http_upgrade;
        # proxy_set_header Connection "upgrade";
    }
}
EOF

# Test the Nginx configuration
echo "🔍 Testing Nginx configuration..."
nginx -t || handle_error "Nginx configuration test failed"

# Enable and start Nginx service
echo "🚀 Starting Nginx service..."
systemctl enable nginx
systemctl restart nginx || handle_error "Failed to start Nginx"

echo ""
echo "✅=== Nginx Proxy Setup Complete ===✅"
echo "🌐 API is now available at:"
echo "http://$FULL_DOMAIN_NAME (port 80) → forwarded to → http://$FULL_DOMAIN_NAME:8000"
echo "📝 You may need to edit \"/etc/nginx/nginx.conf\" to add this line inside the http block:"
echo "    include /etc/nginx/conf.d/*.conf;"
echo ""