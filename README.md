# Digitransit & Matomo (Tag Manager)

This project is aimed at tracking Digitransit user interactions in a GDPR compliant 
manner with a custom Matomo installation. The tracked interactions are based on an 
[interaction concept developed by HSL](https://docs.google.com/spreadsheets/d/1kSf225cstroNrUkPvj5cn4zrWHnMWrtUUdveKLW8zbQ/edit#gid=0).

This project provides 
* a step-by-step tutorial on how to set up your own Matomo server.
* a tutorial how to import existing MTM container data.
* a Python script which enables you to change properties in an exported MTM container file.
* an exported MTM container sample file for Digitransit.

## Run local Matomo server via official docker image

The db.env, matomo.conf and docker-compose files are from the official [Matomo-Docker GitHub repo](https://github.com/matomo-org/docker/tree/master/.examples/nginx).

### Installation
1. set the variables
    * username, password and database name should be the same in the files so as to create the connection  
    * in the db.env file
        * MATOMO_DATABASE_USERNAME
        * MATOMO_DATABASE_PASSWORD
        * MATOMO_DATABASE_DBNAME
    * and in the docker-compose.yml file
        * MYSQL_USER
        * MYSQL_PASSWORD
        * MYSQL_DATABASE
        * MYSQL_ROOT_PASSWORD
2. run command `docker-compose up` in the directory
3. open localhost:8080 in browser -> should see Matomo local installation page
4. follow the installation steps
    * database setup: set by default (use MATOMO_DATABASE_USERNAME, MATOMO_DATABASE_PASSWORD and MATOMO_DATABASE_DBNAME)
    * create super user: you won't be able to modify the super user's username later (you'll be able to add other users)
    * create website: all of the here and now given data can be changed later

### If you get an error after installation
The error messages are quite clear in Matomo.

If you have to modify the _piwik/config/config.ini.php_ file:
1. `docker ps`
2. `docker exec -it <matomo:fpm-alpine container id> sh`
3. `vi config/config.ini.php`
4. Modify the `trusted_hosts[]` property either by modifying one of the given values or add a new one.
5. Save and refresh the browser page.

### Before reinstallation
Docker-compose uses volumes. Any time you'd like to have a fresh start, you have to delete the containers and the volumes too.
See volumes: `docker volume ls`
Delete volumes: `docker volume rm <volume>`

## Use Tag Manager
### Create container
1. in the browser: log in with created superuser
2. activate Tag Manager
3. create a new container (you might have to refresh the page)
4. copy the install code of the container into an appropriate place of the source code (best is a snippet which appears 
on all sites, for example an overall header)

### Add existing container data
_see Export and import first_ 
1. click on Versions, then Import
2. copy your own importReady_ json file, give it a name and save
3. create a new version

## Export and import
When you export a version from an existing container, the exported JSON file will have some container specific properties. It is no problem when you'd like to use it as a backup to the same container but if you'd like to import it to another, you have to make some changes beforehand.
Using the python script you can customize the old, foreign data to your new container. Run the following command:
```
MATOMO_IDCONTAINER=<containerid> MATOMO_IDSITE=<siteid> MATOMO_MATOMOURL=<url> python modify_container_data.py <source_file_name>
```
where
* IDCONTAINER is the container ID (it is under the name of the container on the Tag Manager/Dashboard site)
* IDSITE is the ID of the site (you can find it in Administration/Websites/Manage)
* MATOMOURL will be http://localhost:8080/ locally or the URL of the running Matomo server
* the source_file_name is the file you exported from the older container / the one you downloaded from here

## The example Digitransit MTM file
There is an _exampleMIHcontainer.json_ file which was created for the tracking of the 
[mobil-in-herrenberg.de](https://mobil-in-herrenberg.de) site - based on [HSL's Digitransit project](https://github.com/hsldevcom/digitransit-ui).
If you use another configuration of the Digitransit project, this might be useful for you. But pay attention:
there must be numerous places where your website differ and therefore the tracking events won't be the same.
Use this file for testing Matomo Tag Manager services and to see some examples.
Also, if you'd find a better solution for any of the events, we'd be happy to hear about it!

### What does our container track?
* source and destination search
* travel mode selection (public transport, bicycle, walking, park&ride)
* transport mode selection (bus, rail, subway, carpool)
* favourites: add, edit, save
* other itinerary settings:
    * add, remove via point
    * edit journey date
    * highlight itinerary, open details
    * set journey time (earlier, now, later)
    * switch journey points order
* open, save, reset extra settings
* navigation to the home page
* open route, stop details
* language selection
* ...
