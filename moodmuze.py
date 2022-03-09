#!/usr/bin/env python3

#### Imported Packages ####
from os.path import exists #check if file exists
import os #run os commands
import configparser #config file
import datetime #for datetime in log entries
import sys #exit
import getopt #parameters
import json #handle json data
import re #regular expression

#### Global Variables
## Constants
SELF_INFO = '/etc/moodmuze/moodmuze.info'
cmd = "sed -e '/SELF_NAME=/!d' -e 's/SELF_NAME=//' " + SELF_INFO
SELF_NAME = os.popen(cmd).read().strip()
cmd = "sed -e '/SELF_MAJOR=/!d' -e 's/SELF_MAJOR=//g' " + SELF_INFO
SELF_MAJOR = os.popen(cmd).read().strip()
cmd = "sed -e '/SELF_MINOR=/!d' -e 's/SELF_MINOR=//g' " + SELF_INFO
SELF_MINOR = os.popen(cmd).read().strip()
cmd = "sed -e '/SELF_CONF=/!d' -e 's/SELF_CONF=//g' " + SELF_INFO
SELF_CONF = os.popen(cmd).read().strip()
## Integers
## Booleans

#### Help_Text ####
def Help_Text():
  print( SELF_NAME + ' V' + SELF_MAJOR + '.' + SELF_MINOR + ' Help Text placeholder')

#### Load_Conf ####
def Load_Conf():
  global LOG_FILE
  global LOG_LEVEL
  global BRIDGE_IP
  global AUTH_FILE
  conf_exists = exists(SELF_CONF)
  if conf_exists != True:
    dt = datetime.datetime.now()
    sys.exit(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [ERROR]    Unable to find config file: ' + SELF_CONF + '! Exiting!!!')
  config = configparser.ConfigParser()
  config.read(SELF_CONF)
  # Load Configuration Options
  LOG_FILE = config.get('Log', 'LOG_FILE')
  LOG_LEVEL = int(config.get('Log', 'LOG_LEVEL'))
  BRIDGE_IP = config.get('Hue', 'BRIDGE_IP')
  AUTH_FILE = config.get('Hue', 'AUTH_FILE')

#### Log_Message ####
def Log_Message(level, message):
  dt = datetime.datetime.now()
  if level == 5:
    label = 'INFO'
  elif level == 4:
    label = 'ERROR'
  elif level == 3:
    label = 'WARN'
  elif level == 2:
    label = 'INFO'
  elif level == 1:
    label = 'DEBUG'
  log = open(LOG_FILE, 'a')
  if LOG_LEVEL == 1:
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + str(message), file = log)
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + str(message))
  elif level >= LOG_LEVEL:
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + str(message), file = log)
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + str(message))
  log.close()

#### json_extract ####
# Recursively fetch values from nested JSON
def json_extract(obj, key):
  arr = []
  # Recursively search for values of key in JSON tree
  def extract(obj, arr, key):
    if isinstance(obj, dict):
      for k, v in obj.items():
        if isinstance(v, (dict, list)):
          extract(v, arr, key)
        elif k == key:
          arr.append(v)
    elif isinstance(obj, list):
      for item in obj:
        extract(item, arr, key)
    return arr

#### Parameters ####
def Parameters(argv):
  try:
    opts, args = getopt.getopt(argv, "hd",["help","debug"])
  except getopt.GetoptError:
    Help_Text()
    print('Invalid argument used')
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      Help_Text()
      sys.exit(0)
    elif opt in ('-d', '--debug'):
      LOG_LEVEL = 1
      Log_Message (1, "Debug Logging enabled.")

#### Auth ####
def Auth():
  # Check that auth file exists
  auth_exists = exists(AUTH_FILE)
  if auth_exists == True:
    with open(AUTH_FILE, 'r') as file:
      USERNAME = file.read().rstrip()
  else:
    Log_Message(4, 'Athentication file is missing!')
    sys.exit('Auth Missing')
  # Load Auth Token
  global AUTH_TOKEN
  cmd = "cat " + AUTH_FILE
  AUTH_TOKEN = os.popen(cmd).read().strip()

#### #### Class Bridge #### ####
class Bridge:
  def __init__(self):
    self.token = BRIDGE_IP + '/api/' + AUTH_TOKEN
    self.name = ''
    self.zigbeechannel = ''
    self.bridgeid = ''
    self.mac = ''
    self.dhcp = ''
    self.ipaddress = ''
    self.netmask = ''
    self.gateway = ''
    self.proxyaddress = ''
    self.proxyport = ''
    self.UTC = ''
    self.localtime = ''
    self.timezone = ''
    self.modelid = ''
    self.datastoreversion = ''
    self.swversion = ''
    self.apiversion = ''
    self.swupdate = '' #dict
    self.swupdate2 = ''
    self.linkbutton = ''
    self.portalservices = ''
    self.portalconnection = ''
    self.portalstate = '' #dict
    self.internetservices = '' #dict
    self.factorynew = ''
    self.replacesbridgeid = ''
    self.backup = '' #dict
    self.starterkitid = ''
    self.whitelist = '' #dict

  # Validate response of API interaction
  def check_response(self, data):
    if bool(re.match('\[{"error":{', data)):
      json_error = json.loads(data)
      # Example error [{'error': {'type': 1, 'address': '/', 'description': 'unauthorized user'}}]
      #er_type = json_extract(json_error, 'type')
      #er_address = json_extract(json_error, 'address')
      #er_description = json_extract(json_error, 'description')
      #print(str(er_description + ' at ' + er_address + ' type: ' + er_type))
      Log_Message(4, str(json_error))
      sys.exit('Error Occurred')

  # Pull bridge config
  def pull_config(self):
    cmd = "curl " + self.token
    data = os.popen(cmd).read().strip()
    self.check_response(data)

#### ==== Main Sequence ==== ####
Load_Conf()
Parameters(sys.argv[1:])
Auth()
myBridge = Bridge()
myBridge.pull_config()
