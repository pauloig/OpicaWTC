FROM nginxinc/nginx-unprivileged:1-alpine
LABEL maintainer="agcommunicationsinc.com"

COPY ./default.conf.tpl /etc/nginx/default.conf.tpl
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./run.sh /run.sh

ENV LISTEN_PORT=8000
ENV APP_HOST=app
ENV APP_PORT=9000

USER root

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    touch /etc/nginx/conf.d/default.conf && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x /run.sh

RUN apk update && apk add --no-cache openssl

RUN apk update && apk add --no-cache certbot

# For Let's Encrypt - obtain and renew certificates
RUN certbot certonly --nginx -d appopica.org --non-interactive --agree-tos -m paulo.ismalej@gmail.com 

VOLUME /vol/static

USER nginx

CMD ["/run.sh"]