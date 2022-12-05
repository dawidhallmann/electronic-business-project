# Electronic business project

## How to run?
Please extract files from your dump to `src` folder. There should be two folders for mysql volume and for presta shop volume. The structure should look like the following: 
```sh
src
|-mysql-vol
|-presta-vol
```
Contents of those files are not included in the repository, for obvious reasons :) To run dev-environment just type:

```sh
docker-compose -f docker-compose-dev.yml up --build
```

## Login route
Admin Url: `http://localhost:8080/admin-login` \
Admin email: `admin@admin.com`  \
Admin password: `EtiPg2022`

## Store route
Url: `http://localhost:8080/admin`