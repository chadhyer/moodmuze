#!/usr/bin/env python3

#### Imported Packages
from os.path import exists #check if file exists
import os #run os commands
import configparser #config file
import datetime #for datetime in log entries
import sys #exit
import getopt #parameters
import json #handle json data
import re #regular expression
import requests #api interactions
from pprint import pprint #allows printing object variables

#### Global Variables
## Constants
SELF_INFO = '/etc/moodmuze/moodmuze.info'
ENCODING = 'utf-8'
with open(SELF_INFO, 'r') as INFO:
  for line in INFO:
    if re.search('^SELF_INFO=', line):
      SELF_NAME = line[10:-1]
    elif re.search('^SELF_MAJOR=', line):
      SELF_MAJOR = line[11:-1]
    elif re.search('^SELF_MINOR=', line):
      SELF_MINOR = line[11:-1]
    elif re.search('^SELF_PATCH=', line):
      SELF_PATCH = line[11:-1]
    elif re.search('^SELF_CONF=', line):
      SELF_CONF = line[10:-1]
  INFO.close()
## Integers
## Booleans
print_info = False
print_lights = False
print_groups = False
## Strings
task_lid = ''
task_gid = ''
task_state = ''
task_value = ''

def help_():
  print( SELF_NAME + ' V' + SELF_MAJOR + '.' + SELF_MINOR)
  README = open('./README.md', 'r')
  print(README.read())

def load_conf():
  global LOG_FILE
  global LOG_LEVEL
  global BRIDGE_IP
  global AUTH_FILE
  conf_exists = exists(SELF_CONF)
  if conf_exists != True:
    dt = datetime.datetime.now()
    sys.exit(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [ERROR]    Unable to \
             find config file: ' + SELF_CONF + '! Exiting!!!')
  config = configparser.ConfigParser()
  config.read(SELF_CONF)
  # Load Configuration Options
  LOG_FILE = config.get('Log', 'LOG_FILE')
  LOG_LEVEL = int(config.get('Log', 'LOG_LEVEL'))
  BRIDGE_IP = config.get('Hue', 'BRIDGE_IP')
  AUTH_FILE = config.get('Hue', 'AUTH_FILE')

# Logs app state into log 
def log_message(level, message):
  dt = datetime.datetime.now()
  if level == 5 or level == 2:
    label = 'INFO'
  elif level == 4:
    label = 'ERROR'
  elif level == 3:
    label = 'WARN'
  elif level == 1:
    label = 'DEBUG'
  log = open(LOG_FILE, 'a')
  if LOG_LEVEL == 1:
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' \
          + str(msg), file = log)
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' \
          + str(message))
  elif level >= LOG_LEVEL:
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' \
          + str(message), file = log)
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' \
          + str(message))
  log.close()

# Parameters used when executing script
def parameters(argv):
  global print_info
  global print_lights
  global print_groups
  global task_lid
  global task_gid
  global task_state
  global task_value
  try:
    opts, args = getopt.getopt(argv,"hdBLl:Gg:s:v:",
                               ["help","debug","bridge","lid-info","lid=",
                                "gid-info","git=","state=","value="])
  except getopt.GetoptError:
    help_()
    sys.exit('Invalid argument!')
  for opt, arg in opts:
    if opt in ('-h', '--help'): # Print help text and exit
      help_()
      sys.exit(0)
    elif opt in ('-d', '--debug'): # Enter debug mode
      LOG_LEVEL = 1
      log_message (1, "Debug logging enabled via parameter")
    elif opt in ('-B', '--bridge'): # Return bridge information
      print_info = True
    elif opt in ('-L', '--lid-info'): # Return Light(s) information
      print_lights = True
    elif opt in ('-l', '--lid'): # Light(s) to modify
      task_lid = arg
    elif opt in ('-G', '--gid-info'): # Return Group(s) information
      print_groups = True
    elif opt in ('-g', '--gid'): # Group(s) to modify
      task_gid = arg
    elif opt in ('-s', '--state'): # Change state of Light/Group
      task_state = str(arg)
    elif opt in ('-v', '--value'): # Value applied to state change
      task_value = arg

# Create AUTH_TOKEN variable used to communicate with API
def auth():
  global AUTH_TOKEN
  auth_exists = os.path.exists(AUTH_FILE)
  if auth_exists is True:
    with open(AUTH_FILE, 'r') as file:
      USERNAME = file.read().rstrip()
  else:
    log_message(4, 'Athentication file is missing!')
    sys.exit('Auth Missing')
  # Load Auth Token
  AUTH_TOKEN = 'http://' + BRIDGE_IP + '/api/' + USERNAME

# Validate API interaction was successful
def check_response(data):
  if bool(re.match('\[{"error":{', data)):
    json_error = json.loads(data)
    # Example error [{'error': {'type': 1, 'address': '/', 'description': ' \
    #               unauthorized user'}}]
    log_message(4, str(json_error))
    sys.exit('Error Occurred')
    # Should add error handling - once I know what kind of errors can appear
  else:
    return True

#### Class Light
class Light:
  # When creating class object save all info into variables
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

  # Load state dict into state variables
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

#### Class Group
class Group:
  # When creating class object save all info into variables
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

  # Load action dict into action variables
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

  # Load state dict into state variables
  def load_state(self, data):
    state = json.loads(json.dumps(data))
    self.all_on = state["all_on"]
    self.any_on = state["any_on"]

#### Class Bridge
class Bridge:
  # When creating class object pull data from bridge and save it 
  # into variables
  def __init__(self):
    # Pull bridge config
    url = AUTH_TOKEN + '/config'
    response = requests.get(url)
    data = str(response.content, ENCODING)
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
    self.pull_lights()
    self.pull_groups()

    # Print self if -B --bridge flag used
    if print_info is True:
      pprint(vars(self))

    # Print Lights
    if print_lights is True:
      for light in self.lights:
        pprint(vars(light))

    # Print Groups
    if print_groups is True:
      for group in self.groups:
        pprint(vars(group))

  ### INFO PULLING FUNCTIONS
  # Pull info for all lights, save to a list, and crate light class object 
  # for each light
  def pull_lights(self):
    url = AUTH_TOKEN + '/lights'
    response = requests.get(url)
    data = str(response.content, ENCODING)
    check_response(data)
    lights = json.loads(data)
    for light in lights:
      self.lights.append( Light( light, lights[light]) )

  # Pull info for all groups, save to a list, and create group class object 
  # for each group
  def pull_groups(self):
    url = AUTH_TOKEN + '/groups'
    response = requests.get(url)
    data = str(response.content, ENCODING)
    check_response(data)
    groups = json.loads(data)
    for group in groups:
      self.groups.append( Group( group, groups[group]) )

  # Update Light/Group class object's info
  def update_info(self, obj):
    # Check if object is light or group
    if re.search(".*light", obj.type):
      type_ = '/lights/'
    else:
      type_ = '/groups/'
    # Pull and update class state variables
    url = AUTH_TOKEN + type_ + obj.id
    response = requests.get(url)
    data = str(response.content, ENCODING)
    check_response(data)
    info = json.loads(data)
    obj.load_state(info["state"])
    if type_ == '/groups/':
      obj.load_action(info["action"])

  # update_object's state/action
  def update_object(self, obj, body):
    if re.search(".*light", obj.type):
      url = AUTH_TOKEN + '/lights/' + obj.id + '/state'
    else:
      url = AUTH_TOKEN + '/groups/' + obj.id + '/action'
    response = requests.put(url, body)
    data = str(response.content, ENCODING)
    check_response(data)
    self.update_info(obj)


  ### STATE UPDATING FUNCTIONS
  # Toggle Light/Group on/off then update class object's info
  def toggle_on(self, obj):
    if obj.on is True:
      body = '{"on":false}'
    elif obj.on is False:
      body = '{"on":true}'
    self.update_object(obj, body)

  # Change Brightness (bri) for Light/Group
  # 0 to 255
  def update_bri(self, obj, value):
    if value > 255:
      value = 255
    body = '{"bri":' + str(value) + '}'
    self.update_object(obj, body)

  # Change Hue for Light/Group
  # 0 to 65535
  def update_hue(self, obj, value):
    if value > 65535:
      value = 65535
    body = '{"hue":' + str(value) + '}'
    self.update_object(obj, body)

  # Change Saturation (sat) for Light/Group
  # 0 to 255
  def update_sat(self, obj, value):
    if value > 255:
      value = 255
    body = '{"sat":' + str(value) + '}'
    self.update_object(obj, body)

  # Change effect for Light/Group
  def update_effect(self, obj, value):
    body = '{"effect":"' + value + '"}'
    self.update_object(obj, body)

  # Change xy for Light/Group
  def update_xy(self, obj, value):
    x = value[0]
    y = value[1]
    body = '{"xy": [' + x + ', ' +  y + ']}'
    self.update_object(obj, body)

  # Change ct for Light/Group
  def update_ct(self, obj, value):
    body = '{"ct": ' + value + '}'
    self.update_object(obj, body)

  # Change alert for Light/Group
  #def update_alert(self, obj, value):
  #  pass

  # Change colormode for Light/Group
  def update_colormode(self, obj, value):
    body = '{"colormode": "' + value + '"}'
    self.update_object(obj, body)

  # task
  def task(self):
    if task_lid != '':
      for idx, light in enumerate(self.lights):
        if task_lid == light.id:
          target = self.lights
          target_idx = idx
          target_type = self.lights[target_idx].type
          target_name = self.lights[target_idx].name
    elif task_gid != '':
      for idx, group in enumerate(self.groups):
        if task_gid == group.id:
          target = self.groups
          target_idx = idx
          target_type = self.groups[target_idx].type
          target_name = self.groups[target_idx].name
    if task_state == 'on':
      log_message(2, 'Toggling on state for ' + str(target_name))
      self.toggle_on(target[target_idx])
    elif task_state == 'bri':
      log_message(2, 'Updating brightness for ' + str(target_name))
      self.update_bri(target[target_idx], task_value)
    elif task_state == 'hue':
      log_message(2, 'Updating hue for ' + str(target_name))
      self.update_hue(target[target_idx], task_value)
    elif task_state == 'sat':
      log_message(2, 'Updating saturation for ' + str(target_type))
      self.update_sat(target[target_idx], task_value)
    elif task_state == 'effect':
      log_message(2, 'Updating effect for ' + str(target_name))
      self.update_effect(target[target_idx], task_value)
    elif task_state == 'xy':
      log_message(2, 'Updating xy for ' + str(target_name))
      self.update_xy(target[target_idx], task_value)
    elif task_state == 'ct':
      log_message(2, 'Updating ct for ' + str(target_name))
      self.update_ct(target[target_idx], task_value)
    #elif task_state == 'alert':
    #  log_message(2, 'Updating alert for ' + str(target_name))
    #  self.update_alert(target[target_idx], task_value)
    elif task_state == 'colormode':
      log_message(2, 'Updating colormode for ' + str(target_name))
      self.update_colormode(target[target_idx], task_value)

# Main Sequence
load_conf()
log_message(5, 'Initiating ' + SELF_NAME + ' v' + SELF_MAJOR + SELF_MINOR + \
            SELF_PATCH )
parameters(sys.argv[1:])
auth()
MyBridge = Bridge()
if task_state != '':
  MyBridge.task()
