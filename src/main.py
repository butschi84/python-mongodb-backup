import os, time, subprocess, pymongo
from modules.logger import OpensightLogger
from modules.mongodb import Mongo
from datetime import date

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials

# settings
settings = {
    "gcloud_project": os.environ.get("gcloud_project"),
    "gcloud_bucket": os.environ.get("gcloud_bucket"),
    "mongo_username": os.environ.get("mongo_username"),
    "mongo_password": os.environ.get("mongo_password"),
    "mongo_server": os.environ.get("mongo_server")
}

# initialize logging
logger = OpensightLogger()
log = logger.getLogger()

# init message
log.info("mongodb backup")
log.info("==========================================")
log.info("V 1.0")
log.info("gcloud_bucket: {}".format(settings["gcloud_bucket"]))
log.info("mongo_username: {}".format(settings["mongo_username"]))
log.info("mongo_password: {}".format(settings["mongo_password"]))
log.info("mongo_server: {}".format(settings["mongo_server"]))

# initialize objects
mongo = Mongo(
    log, 
    username=settings["mongo_username"],
    password=settings["mongo_password"],
    server=settings["mongo_server"])

# gcloud authentication
# ===================================
log.info("gcloud authentication")
client = storage.Client.from_service_account_json("/usr/src/app/sa.json")
# client = storage.Client.from_service_account_json("sa.json")
bucket = client.get_bucket(settings["gcloud_bucket"])

# initialize mongodb client
# ===================================
log.info("initialize mongodb client...")
databases = mongo.getDatabases()

for database in databases:
    log.info("processing database: {}".format(database["name"]))
    # get todays date
    log.info("=> fetching today's date and filename")
    today = date.today()
    formatedDate = today.strftime("%Y-%m-%d")
    filename = "{}_{}.gz".format(formatedDate, database["name"])
    log.info("=> {}".format(filename))
    
    # execute mysql dump
    log.info("=> create mongodb dump for database: {}".format(database["name"]))
    mongo.createDump(database["name"], filename)

    # upload to google blob storage
    log.info("=> upload to gcloud: {}".format(filename))
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)