FROM nginx:stable-alpine 

COPY ./nginxConf.production.conf etc/nginx/nginx.conf
COPY ./nginxDefault.production.conf /etc/nginx/conf.d/default.conf 
CMD ["nginx", "-g", "daemon off;"]