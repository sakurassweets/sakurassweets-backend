FROM postgres:12-alpine

# Copy maintenance
COPY ./compose/production/postgres/maintenance /usr/production/bin/maintenance

# Chmod maintenance all files
RUN chmod +x /usr/production/bin/maintenance/*

# Move maintenance to /usr/production/bin and remove old maintenance directory
RUN mv /usr/production/bin/maintenance/* /usr/production/bin \
    && rmdir /usr/production/bin/maintenance