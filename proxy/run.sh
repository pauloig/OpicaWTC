#!/bin/sh

set -e
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# For Let's Encrypt - obtain and renew certificates
certbot certonly -v --nginx -d appopica.org --non-interactive --agree-tos -m paulo.ismalej@gmail.com

nginx -g 'daemon off;'
