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
  auth = os.popen(cmd).read().strip()
  AUTH_TOKEN = BRIDGE_IP + '/api/' + auth

# Validate response of API interaction
def check_response(data):
  if bool(re.match('\[{"error":{', data)):
    json_error = json.loads(data)
    # Example error [{'error': {'type': 1, 'address': '/', 'description': 'unauthorized user'}}]
    #er_type = json_extract(json_error, 'type')
    #er_address = json_extract(json_error, 'address')
    #er_description = json_extract(json_error, 'description')
    #print(str(er_description + ' at ' + er_address + ' type: ' + er_type))
    Log_Message(4, str(json_error))
    sys.exit('Error Occurred')

#### #### Class Light #### ####
class Light:
  def __init__(self, lid, data):
    self.id = lid
    self.info = json.loads(json.dumps(data))
    # Extract info to variables
    self.load_state(self.info["state"]) #dict
    #try:
    #  self.swupdate = self.info["swupdate"] #dict
    #except:
    #  self.swupdate = None
    try:
      self.type = self.info["type"]
    except:
      self.type = None
    try:
      self.name = self.info["name"]
    except:
      self.name = None
    try:
      self.modelid = self.info["modelid"]
    except:
      self.modelid = None
    #try:
    #  self.manufacturername = self.info["manufacturername"]
    #except:
    #  self.manufacturername = None
    try:
      self.productname = self.info["productname"]
    except:
      self.productname = None
    #try:
    #  self.capabilities = self.info["capabilities"] #dict
    #except:
    #  self.capabilities = None
    #try:
    #  self.config = self.info["config"] #dict
    #except:
    #  self.config = None
    try:
      self.uniqueid = self.info["uniqueid"]
    except:
      self.uniqueid = None
    #try:
    #  self.swversion = self.info["swversion"]
    #except:
    #  self.swversion = None
    #try:
    #  self.swconfigid = self.info["swconfigid"]
    #except:
    #  self.swconfigid = None
    #try:
    #  self.productid = self.info["productid"]
    #except:
    #  self.productid = None

  # Load State
  def load_state(self, data):
    state = json.loads(json.dumps(data))
    self.on = state["on"]
    self.bri = state["bri"]
    try:
      self.hue = state["hue"]
    except:
      self.hue = None
    try:
      self.sat = state["sat"]
    except:
      self.sat = None
    try:
      self.effect = state["effect"]
    except:
      self.effect = None
    try:
      self.xy = state["xy"]
    except:
      self.xy = None
    self.ct = state["ct"]
    self.alert = state["alert"]
    self.colormode = state["colormode"]
    self.mode = state["mode"]
    self.reachable = state["reachable"]

#### #### Class Group #### ####
class Group:
  def __init__(self, lid, data):
    self.id = lid
    self.info = json.loads(json.dumps(data))
    # Extract info to variables
    self.name = self.info["name"]
    self.lights = self.info["lights"] # list
    #self.sensors = self.info["sensors"] # list
    self.type = self.info["type"]
    self.load_state(self.info["state"])
    #self.recycle = self.info["recycle"]
    #self.clss = self.info["clss"]
    #self.locations = self.info["locations"]
    self.load_action(self.info["action"]) # dict

  def load_action(self, data):
    action = json.loads(json.dumps(data))
    self.on = action["on"]
    self.bri = action["bri"]
    try:
      self.hue = action["hue"]
    except:
      self.hue = None
    try:
      self.sat = action["sat"]
    except:
      self.sat = None
    try:
      self.effect = action["effect"]
    except:
      self.effect = None
    try:
      self.xy = action["xy"]
    except:
      self.xy = None
    self.ct = action["ct"]
    self.alert = action["alert"]
    self.colormode = action["colormode"]

  def load_state(self, data):
    state = json.loads(json.dumps(data))
    self.all_on = state["all_on"]
    self.any_on = state["any_on"]

#### #### Class Bridge #### ####
class Bridge:
  def __init__(self):
    # Pull bridge config
    cmd = "curl " + AUTH_TOKEN + "/config"
    data = os.popen(cmd).read().strip()
    check_response(data)
    self.config = json.loads(data)
    # Extract config to variables
    self.name = self.config["name"]
    self.zigbeechannel = self.config["zigbeechannel"]
    self.bridgeid = self.config["bridgeid"]
    self.mac = self.config["mac"]
    self.dhcp = self.config["dhcp"]
    self.ipaddress = self.config["ipaddress"]
    self.netmask = self.config["netmask"]
    self.gateway = self.config["gateway"]
    self.proxyaddress = self.config["proxyaddress"]
    self.proxyport = self.config["proxyport"]
    self.UTC = self.config["UTC"]
    self.localtime = self.config["localtime"]
    self.timezone = self.config["timezone"]
    self.modelid = self.config["modelid"]
    self.datastoreversion = self.config["datastoreversion"]
    self.swversion = self.config["swversion"]
    self.apiversion = self.config["apiversion"]
    self.swupdate = self.config["swupdate"] #dict
    self.swupdate2 = self.config["swupdate2"]
    self.linkbutton = self.config["linkbutton"]
    self.portalservices = self.config["portalservices"]
    self.portalconnection = self.config["portalconnection"]
    self.portalstate = self.config["portalstate"] #dict
    self.internetservices = self.config["internetservices"] #dict
    self.factorynew = self.config["factorynew"]
    self.replacesbridgeid = self.config["replacesbridgeid"]
    self.backup = self.config["backup"] #dict
    self.starterkitid = self.config["starterkitid"]
    self.whitelist = self.config["whitelist"] #dict
    self.lights = []
    self.groups = []

  # Pull Light List
  def pull_lights(self):
    cmd = "curl " + AUTH_TOKEN + "/lights"
    data = os.popen(cmd).read().strip()
    check_response(data)
    lights = json.loads(data)
    for light in lights:
      #print(light)
      #print(lights[light])
      self.lights.append( Light(light, lights[light]) )
    #for obj in self.lights:
    #  print( obj.name, obj.id, obj.on, obj.bri, obj.hue, obj.sat )

  # Pull Light List
  def pull_groups(self):
    cmd = "curl " + AUTH_TOKEN + "/groups"
    data = os.popen(cmd).read().strip()
    check_response(data)
    groups = json.loads(data)
    for group in groups:
      #print(group)
      #print(groups[group])
      self.groups.append( Group(group, groups[group]) )
    #for obj in self.groups:
    #  print( obj.name, obj.id, obj.all_on, obj.any_on )

  # Toggle Light/Group on/Off
  def toggle_on(self, lid, gid):
    if lid is not None and gid is None:
      cmd = "curl " + AUTH_TOKEN + "/lights/" + lid + '/state'
      if lig.on == false:
        cmd = "curl -X PUT " + AUTH_TOKEN + "/lights/" + lid + '/state -d \'{"on":true}\''
      elif lig.on == true:
        cmd = "curl -X PUT " + AUTH_TOKEN + "/lights/" + lid + '/state -d \'{"on":false}\''
    elif lid is None and gid is not None:
      cmd = "curl " + AUTH_TOKEN + "/groups/" + gid + '/state'
    else:
      Log_Message(3, 'Illegal usage of toggle_on')

#### ==== Main Sequence ==== ####
Load_Conf()
Parameters(sys.argv[1:])
Auth()
myBridge = Bridge()
#myBridge.pull_lights()
#myBridge.pull_groups()
