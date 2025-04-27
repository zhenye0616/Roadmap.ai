# frontend/Dockerfile
FROM nginx:alpine

# Copy our custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static assets
COPY . /usr/share/nginx/html

EXPOSE 80