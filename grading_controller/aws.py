"""
Production configuration for grading controller
"""
import json
import os

from .logsettings import get_logger_config
from .settings import *
import logging

######################################################################
#General config



######################################################################
#Read config from json file
with open(ENV_ROOT / "env.json") as env_file:
    ENV_TOKENS = json.load(env_file)

#Debug
DEBUG = ENV_TOKENS.get('DEBUG', False)
if isinstance(DEBUG,basestring):
    DEBUG= DEBUG.lower()=="true"
TEMPLATE_DEBUG = ENV_TOKENS.get('TEMPLATE_DEBUG', False)
if isinstance(TEMPLATE_DEBUG,basestring):
    TEMPLATE_DEBUG= TEMPLATE_DEBUG.lower()=="true"
PRINT_QUERIES = ENV_TOKENS.get('PRINT_QUERIES', False)
if isinstance(PRINT_QUERIES,basestring):
    PRINT_QUERIES= PRINT_QUERIES.lower()=="true"

#General
REQUESTS_TIMEOUT = int(ENV_TOKENS.get('REQUESTS_TIMEOUT', REQUESTS_TIMEOUT))
TIME_BETWEEN_XQUEUE_PULLS = int(ENV_TOKENS.get('TIME_BETWEEN_XQUEUE_PULLS', TIME_BETWEEN_XQUEUE_PULLS))
TIME_BETWEEN_EXPIRED_CHECKS = int(ENV_TOKENS.get('TIME_BETWEEN_EXPIRED_CHECKS', TIME_BETWEEN_EXPIRED_CHECKS))
GRADER_SETTINGS_DIRECTORY = ENV_TOKENS.get('GRADER_SETTINGS_DIRECTORY')
MAX_NUMBER_OF_TIMES_TO_RETRY_GRADING = int(ENV_TOKENS.get('MAX_NUMBER_OF_TIMES_TO_RETRY_GRADING'))

#ML
MIN_TO_USE_ML = int(ENV_TOKENS.get('MIN_TO_USE_ML', MIN_TO_USE_ML))
ML_MODEL_PATH = os.path.join(ENV_ROOT, ENV_TOKENS.get('ML_MODEL_PATH'))
TIME_BETWEEN_ML_CREATOR_CHECKS = int(ENV_TOKENS.get('TIME_BETWEEN_ML_CREATOR_CHECKS', TIME_BETWEEN_ML_CREATOR_CHECKS))
TIME_BETWEEN_ML_GRADER_CHECKS = int(ENV_TOKENS.get('TIME_BETWEEN_ML_GRADER_CHECKS', TIME_BETWEEN_ML_GRADER_CHECKS))
USE_S3_TO_STORE_MODELS= ENV_TOKENS.get('USE_S3_TO_STORE_MODELS', USE_S3_TO_STORE_MODELS)
if isinstance(USE_S3_TO_STORE_MODELS,basestring):
    USE_S3_TO_STORE_MODELS= USE_S3_TO_STORE_MODELS.lower()=="true"
S3_BUCKETNAME=ENV_TOKENS.get('S3_BUCKETNAME',"OpenEnded")

#Peer
MIN_TO_USE_PEER = int(ENV_TOKENS.get('MIN_TO_USE_PEER', MIN_TO_USE_PEER))
PEER_GRADER_COUNT = int(ENV_TOKENS.get('PEER_GRADER_COUNT', PEER_GRADER_COUNT))
PEER_GRADER_MINIMUM_TO_CALIBRATE = int(ENV_TOKENS.get("PEER_GRADER_MINIMUM_TO_CALIBRATE", PEER_GRADER_MINIMUM_TO_CALIBRATE))
PEER_GRADER_MAXIMUM_TO_CALIBRATE = int(ENV_TOKENS.get("PEER_GRADER_MAXIMUM_TO_CALIBRATE", PEER_GRADER_MAXIMUM_TO_CALIBRATE))
PEER_GRADER_MIN_NORMALIZED_CALIBRATION_ERROR = float(ENV_TOKENS.get("PEER_GRADER_MIN_NORMALIZED_CALIBRATION_ERROR", PEER_GRADER_MIN_NORMALIZED_CALIBRATION_ERROR))

#Submission Expiration
EXPIRE_SUBMISSIONS_AFTER = int(ENV_TOKENS.get('EXPIRE_SUBMISSIONS_AFTER', EXPIRE_SUBMISSIONS_AFTER))
RESET_SUBMISSIONS_AFTER = int(ENV_TOKENS.get('RESET_SUBMISSIONS_AFTER', RESET_SUBMISSIONS_AFTER))

local_loglevel = ENV_TOKENS.get('LOCAL_LOGLEVEL', 'INFO')
LOG_DIR = ENV_TOKENS.get("LOG_DIR", ENV_ROOT / "log")

LOGGING = get_logger_config(LOG_DIR,
    logging_env=ENV_TOKENS['LOGGING_ENV'],
    syslog_addr=(ENV_TOKENS['SYSLOG_SERVER'], 514),
    local_loglevel=local_loglevel,
    debug=DEBUG)

######################################################################
# Read secure config
with open(ENV_ROOT / "auth.json") as auth_file:
    AUTH_TOKENS = json.load(auth_file)

XQUEUE_INTERFACE = AUTH_TOKENS['XQUEUE_INTERFACE']
GRADING_CONTROLLER_INTERFACE = AUTH_TOKENS['GRADING_CONTROLLER_INTERFACE']
DATABASES = AUTH_TOKENS['DATABASES']

AWS_ACCESS_KEY_ID = AUTH_TOKENS.get("AWS_ACCESS_KEY_ID","")
AWS_SECRET_ACCESS_KEY = AUTH_TOKENS.get("AWS_SECRET_ACCESS_KEY","")