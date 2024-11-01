#!/bin/sh

set -e
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf#

USER root

# For Let's Encrypt - obtain and renew certificates
certbot certonly --nginx -d appopica.org --non-interactive --agree-tos -m paulo.ismalej@gmail.com

USER nginx

nginx -g 'daemon off;'
