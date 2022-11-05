import json
import logging

class OpensightLogger:

    __logger = None

    def __init__(self):
        # create logger
        log = logging.getLogger()
        log.setLevel(logging.INFO)

        # create formatter - this formats the log messages accordingly
        logFormatter = logging.Formatter(json.dumps({
            'time': '%(asctime)s',
            'pathname': '%(pathname)s',
            'line': '%(lineno)d',
            'logLevel': '%(levelname)s',
            'message': '%(message)s'
        }))
        consoleFormatter = logging.Formatter('%(asctime)s' + ' - %(levelname)s - %(message)s')

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(consoleFormatter)

        # add handler to logger
        if (log.hasHandlers()):
            log.handlers.clear()
        log.addHandler(consoleHandler)

        self.__logger = log

    def getLogger(self):
        return self.__logger