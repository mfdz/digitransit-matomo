## Run local Matomo server via official docker image

The db.env, matomo.conf and docker-compose files are from the official [Matomo-Docker GitHub repo](https://github.com/matomo-org/docker/tree/master/.examples/nginx).

### Installation
1. set the variables
    * in the db.env file
        * MATOMO_DATABASE_USERNAME
        * MATOMO_DATABASE_PASSWORD
        * MATOMO_DATABASE_DBNAME
    * and in the docker-compose files
        * MYSQL_ROOT_PASSWORD
2. run command `docker-compose up` in the directory
3. database setup (in case you are not using your own mariadb image)
	1. list the running containers: `docker ps`
	2. step into the container of the db: `docker exec -it <mariadb container> sh`
	3. log in to the mysql as root: `mysql -u root -p`, then add <MYSQL_ROOT_PASSWORD> as password
	4. create database: `CREATE DATABASE <MATOMO_DATABASE_DBNAME>;`
		* check: `SHOW DATABASES;`
	5. create user: `CREATE USER '<MATOMO_DATABASE_USERNAME>'@'%' IDENTIFIED BY '<MATOMO_DATABASE_PASSWORD>';`
		* check: `select user,host from mysql.user;`
	6. add privileges for user: `GRANT ALL PRIVILEGES ON * . * TO '<MATOMO_DATABASE_USERNAME>'@'%';`
		* _important: Database user must have the following privileges: CREATE, ALTER, SELECT, INSERT, UPDATE, DELETE, DROP, CREATE TEMPORARY TABLES._
		* check: `SHOW GRANTS [FOR <MATOMO_DATABASE_USERNAME>]`
	7. save user privilege modifications: `FLUSH PRIVILEGES;`
4. open localhost:8080 in browser -> Matomo local installation page
5. follow the installation steps
    * database setup: set by default (use MATOMO_DATABASE_USERNAME or root, MATOMO_DATABASE_PASSWORD or MYSQL_ROOT_PASSWORD and MATOMO_DATABASE_DBNAME)
    * create website: all of the here and now given data can be changed later

### If you get an error after installation
The error messages are quite clear in Matomo.

If you have to modify the piwik/config/config.ini.php file:
1. `docker ps`
2. `docker exec -it <matomo:fpm-alpine container id> sh`
3. `vi config/config.ini.php`
4. Modify the `trusted_hosts[]` property either by modifying one of the given values or add a new one.
5. Save and refresh the browser page.

### Before reinstallation
Docker-compose uses volumes. Any time you'd like to have a fresh start, you have to delete the containers and the volumes too.
See volumes: `docker volume ls`
Delete volumes: `docker volume rm <volume>`

## Use Tag Manager: create container with existing data
1. in the browser log in with created superuser
2. activate Tag Manager
3. create a new container (you might have to refresh the page)
4. copy the install code of the container into the UI
4. click on Versions, then Import
5. copy the importReady_ json file, give it a name and save
6. create a new version

## Export and import
When you export a version from an existing container, the exported JSON file will have some container specific properties. It is no problem when you'd like to use it as a backup to the same container but if you'd like to import it to another, you have to make some changes beforehand.
Using the mtm_export_modifier python script you can customize the old, foreign data to your new container. Run the following command:
```
MATOMO_IDCONTAINER= MATOMO_IDSITE= MATOMO_MATOMOURL= python mtm_export_modifier.py <source_file_name>
```
where
* IDCONTAINER is the container ID (it is under the name of the container on the Tag Manager/Dashboard site)
* IDSITE is the ID of the site (you can find it in Settings/Websites/Manage)
* MATOMOURL will be http://localhost:8080/ or the URL of the running Matomo server
* the source_file_name is the file you exported from the older container
