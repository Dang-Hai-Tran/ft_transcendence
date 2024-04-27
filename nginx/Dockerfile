FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY ssl /etc/ssl

EXPOSE 443/tcp

ENTRYPOINT [ "nginx" ]
CMD ["-g", "daemon off;"]
