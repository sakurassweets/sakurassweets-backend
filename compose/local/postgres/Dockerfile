FROM postgres:12-alpine

# Copy maintenance
COPY ./compose/local/postgres/maintenance /usr/local/bin/maintenance

# Chmod maintenance all files
RUN chmod +x /usr/local/bin/maintenance/*

# Move maintenance to /usr/local/bin and remove old maintenance directory
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance