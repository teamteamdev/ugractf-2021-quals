FROM alpine
RUN apk add php8-fpm nginx python3

CMD /usr/sbin/php-fpm8 -D -R; nginx -c /nginx.conf -g 'daemon off;'
