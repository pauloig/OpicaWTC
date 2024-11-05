# Redirect HTTP traffic to HTTPS
server {
    listen ${LISTEN_PORT};
    server_name appopica.org www.appopica.org;

    location / {
        return 301 https://$host$request_uri;
    }
}

# Main HTTPS server block
server {
    listen 443 ssl;
    server_name appopica.org www.appopica.org;

    # SSL certificate paths
    ssl_certificate /etc/nginx/ssl/fullchain.crt;
    ssl_certificate_key /etc/nginx/ssl/opica-key.pem;

    # SSL settings for improved security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers HIGH:!aNULL:!MD5;

    proxy_connect_timeout 600s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;
    send_timeout 600s;
    fastcgi_send_timeout 600s;
    fastcgi_read_timeout 600s;

    # Static files
    location /static {
        alias /vol/static;
    }

    # uWSGI application server
    location / {
        uwsgi_read_timeout 600s;
        uwsgi_send_timeout 600s;
        uwsgi_pass ${APP_HOST}:${APP_PORT};
        include /etc/nginx/uwsgi_params;
        client_max_body_size 30M;

        # Add X-Forwarded-Proto for HTTPS detection
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
