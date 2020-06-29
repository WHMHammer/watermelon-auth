#!sh

# Instanciate a database container
docker pull mariadb
docker run --name watermelon_db -p 172.17.0.1:3306:3306 -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -d mariadb

# While Initializing the database, build the back-end image and then instantiate
docker build -t watermelon_back_end back_end
docker run --name watermelon_back_end -p 8080:80 -d watermelon_back_end

# Wait for the database to finish initialization
for i in {5..1..-1}
do
    printf "\rSleeping %ss to wait for the database to finish initialization" "$i"
    sleep 1s
done

# Define the database
docker exec -i watermelon_db mysql -u root < schema.sql

echo "The app will be ready in a minute."
