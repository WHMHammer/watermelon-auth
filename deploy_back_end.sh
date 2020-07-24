#!/bin/sh
# Instanciate a database container
docker pull mariadb
docker run --name watermelon_db -p 172.17.0.1:3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -d mariadb

# While Initializing the database, build the back-end image and then instantiate
docker build -t watermelon_back_end back_end
docker run --name watermelon_back_end -p 8080:80 -d watermelon_back_end

# Wait for the database to finish initialization
echo "Sleeping 5s to wait for the database to finish initialization"
sleep 5s

# Define the database
docker exec -i watermelon_db mysql -u root < schema.sql

echo "The app has started and will be ready in a minute."
