# MySQL docker container

First we need some volumes, one volume for mysql and a separeted volume for the config of mysql.

>`docker volume create mysql`

>`docker volume create mysql_config`

Create a network, so our application can cummunicate with our database.
This is called a user-defined bridge network, provides a DNS lookup services to create our connection string.

>`docker network create mysqlnet`

# Run MySQL container and attach volumes and network

>`docker run --rm -d -v mysql:/var/lib/mysql -v mysql_config:/etc/mysql -p 3306:3306  --network mysqlnet --name mysqldb -e MYSQL_ROOT_PASSWORD=p@ssw0rd1  mysql`

# Connect to the database

>`  docker exec -ti mysqldb mysql -u root -p`

> default password is <strong>p@ssw0rd1</strong>


# Requirements

 >``pip3 install mysql-connector-python``

 >``pip3 freeze | grep mysql-connector-python >> requirements.txt``

 ## Adding Cryptography
> ``import cryptography``

Required for sha256_password or caching_sha2_password auth methods.
Otherwise passwords are given in plaintext accros the network.

# Build image
Now we can build our image.

>``docker build --tag python-docker-dev .``

Add container to database network

>` docker run \
--rm -d \
--network mysqlnet \
--name rest-server \
-p 5000:5000 \
python-docker-dev `

# Curl

 >`curl http://localhost:5000/initdb`

 >`curl http://localhost:5000/widgets`


 # Docker-Compose 

 ## MySQL

 Adding Flask and MySQL database, creating two volumes and setting up the configuration such as the ports and environment-variables.

 `version: '3.8'

services:
 web:
  build:
   context: .
  ports:
  - 5000:5000
  volumes:
  - ./:/app

 mysqldb:
  image: mysql
  ports:
  - 3306:3306
  environment:
  - MYSQL_ROOT_PASSWORD=p@ssw0rd1
  volumes:
  - mysql:/var/lib/mysql
  - mysql_config:/etc/mysql

volumes:
  mysql:
  mysql_config:`

  ## Start using a single command

  >`docker-compose up`
  
  for devops:
 
 > `docker-compose up --force-recreate --remove-orphans`

  > Note: you have to be in the Docker\DatabaseApp directory.


## Adding phpMyadmin 
Able to manage the SQL database


