# Stop and remove containers
echo "Shutting down containers"
docker-compose down -v --rmi all
# Previous line shutdown your containers and remove all objects linked to your hub