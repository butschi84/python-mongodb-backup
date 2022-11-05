import json, subprocess
import logging
import pymongo

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class Mongo(logging.Handler):

    __mongo_username = ""
    __mongo_password = ""
    __mongo_server = ""
    __mongo_uri = ""
    __logger = None
    __mongoClient = None

    def __init__(self, logger, username, password, server):
        self.__mongo_username = username
        self.__mongo_password = password
        self.__mongo_server = server
        self.__logger = logger
        self.__connect()

    def __connect(self, database=""):
        try:
            self.__mongo_uri = "mongodb+srv://{}:{}@{}/{}?authSource=admin&readPreference=primary&ssl=true&tlsAllowInvalidCertificates=true".format(
                self.__mongo_username, 
                self.__mongo_password, 
                self.__mongo_server,
                database)
            self.__mongoClient = pymongo.MongoClient(self.__mongo_uri)
        except Exception as e:
            self.__logger.error("Error in Mongo::__connect()")

    def getDatabases(self):
        try:
            self.__logger.info("get all mongodb databases")
            return list(self.__mongoClient.list_databases())
        except Exception as e:
            self.__logger.error("Error in Mongo::getDatabases()")

    def createDump(self, dbname, outputFileName):
        self.__connect(database=dbname)
        self.__logger.info("start dump of mongo database: {}".format(dbname))
        result = subprocess.run([
            "mongodump",
            "--uri={}".format(self.__mongo_uri),
            "--archive={}".format(outputFileName),
            "--gzip"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.__logger.info(result)