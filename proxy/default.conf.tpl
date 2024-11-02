server {
    listen ${LISTEN_PORT};
    server_name appopica.org;
    location / {
        return 301 https://$host$request_uri;
    }

    proxy_connect_timeout 600s;
    proxy_send_timeout 600s;
    proxy_read_timeout 600s;
    send_timeout       600s;
    fastcgi_send_timeout 600s;
    fastcgi_read_timeout 600s;

    location /static {
        alias /vol/static;

        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout       600s;
        fastcgi_send_timeout 600s;
        fastcgi_read_timeout 600s;
    }

    location / {
        uwsgi_read_timeout 600s;
        uwsgi_send_timeout 600s;
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    30M;

        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout       600s;
        fastcgi_send_timeout 600s;
        fastcgi_read_timeout 600s;
    }
}

server {
    listen 443 ssl;
    server_name appopica.org;

    #ssl_certificate /etc/nginx/ssl/cert.pem;
    #ssl_certificate_key /etc/nginx/ssl/key.pem;

    #location / {
    #    include uwsgi_params;
    #    uwsgi_pass app:8000;  # Ensure this aligns with your uWSGI setup
    #}
}