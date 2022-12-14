# mongodb backup

Backup mongodb databases to google cloud storage.
With this python container, you can run the backup job on your kubernetes cluster as a cronjob.

# General
The tool lists all databases on mongodb atlas and creates backups, which are then uploaded to a gcloud backup datastore.

* list all databases on mongodb atlas
* create backups (gzip)
* upload backups to gcloud

# setup

## gcloud

**GCloud Project ID**<br />
Make note of your gcloud project id.
![](docs/gcloud_projectid.png)

**GCloud Service Account**<br />
In Google Cloud IAM, create a service account with "storage admin" privilege.
Export a key file (sa.json) for the service account. The main.py script needs the sa.json in order to access the bucket on google cloud storage.
![](docs/gcloud_serviceaccount.png)

**GCloud Storage Bucket**<br />
Create a storage bucket on your Google Cloud with settings as you like and make note of the bucket ID.

## mongodb atlas

This tool is made to backup all databases from your mongodb atlas. So you should make note of your servername, username and password.

## Utility Setup
Now you can fill all necessary variables in env.sh and execute the backup utility

```
. ./env.sh
python3 -m pip install -r requirements.txt
python3 src/main.py
```


# MongoDB Backup and Restore (manually)

A short user manual to create manual database dumps and restores
## variable definitions

```
# mongodb server name
export mongo_server=myMongoServer

# mongodb user name
export mongo_username=admin

# mongodb password
export mongo_password=xxxxxxx

# mongodb connection string
export mongo_connectionString="mongodb+srv://${mongo_username}:${mongo_password}@${mongo_server}/?authSource=admin&readPreference=primary&ssl=true&tlsAllowInvalidCertificates=true"

# mongodb db to export
export mongo_dbname=myDBName

# mongodb db to restore to
export mongodb_restoreto=restoreToDB
```

## examples

### db backup

Create a new dump for a database (gzip)

```
 mongodump \
    --uri=$mongo_connectionString \
    --db=$mongo_dbname \
    --archive="${mongo_dbname}.gz" \
    --gzip
```


### db restore to original location

```
mongorestore \
  --gzip \
  --uri $mongo_connectionString \
  --archive=2022-11-03_my_database.gz
```

### db restore to new database

```
mongorestore \
  --gzip \
  --uri $mongo_connectionString \
  --archive="${mongo_dbname}.gz" \
  --nsFrom="${mongo_dbname}.*" \
  --nsTo "${mongodb_restoreto}.*"
```