# Use the official PostgREST image
FROM postgrest/postgrest:latest

# Copy the configuration file
COPY postgrest/postgrest.conf /etc/postgrest.conf

# Expose the default PostgREST port
EXPOSE 3000

# Start PostgREST
CMD ["postgrest", "/etc/postgrest.conf"]