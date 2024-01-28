FROM nginx:1.25.3-alpine-slim

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/local/nginx/nginx.conf /etc/nginx/conf.d
