# BibApp Crawler & DB Application
> This repository stores the code for the BibApp crawler and database application.


Disclaimer
==================
Make sure to create an `.env` file in the toplevel directory and add the following variables:
```
MYSQL_DATABASE=datamining
MYSQL_USER=root
MYSQL_ROOT_PASSWORD=<SET A PASSWORD HERE>
MYSQL_PORT=3306
```

Directory structure
==================
#### `toplevel directory`:
- `docker-compose.yml` file to start the crawler and database application.
- `.env` file to set environment variables. (see disclaimer)
- `.gitignore` file to ignore files that should not be commited to the repository.
- `README.md` file with instructions on how to run the crawler and database application.


#### `src` crawler:
Contains the files for the crawlers.

#### `db` MySQL database:
Contains the files to set up the MySQL database service. 

Setup 
==================
1. Install Docker and [Docker Compose](https://docs.docker.com/compose/install/) on your machine.
2. Clone this repository.
3. Create an `.env` file in the toplevel directory and add the variables (see disclaimer).
4. Unzip the `data.zip` file in the `db` directory.
5. DO NOT forget to set a password for the root user in the `.env` file.
6. Run `docker compose up -d` in the toplevel directory to start the crawler and database application.
7. Optional: when debugging, run `docker compose up --build` to rebuild the images after changes to source files. Else you won't see the changes in the running containers.