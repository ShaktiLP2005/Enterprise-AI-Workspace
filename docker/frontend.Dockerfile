FROM nginx:alpine

# Copy frontend static files

COPY frontend/index.html /usr/share/nginx/html/index.html
COPY frontend/style.css /usr/share/nginx/html/style.css
COPY frontend/app.js /usr/share/nginx/html/app.js

# Configure Nginx reverse proxy

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Expose Nginx

EXPOSE 80