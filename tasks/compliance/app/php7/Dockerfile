FROM alpine
RUN apk add php7-fpm php7-json nginx python3

CMD /usr/sbin/php-fpm7 -D -R; nginx -c /nginx.conf -g 'daemon off;'
