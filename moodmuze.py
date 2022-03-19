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

# Help text
def Help_Text():
  print( SELF_NAME + ' V' + SELF_MAJOR + '.' + SELF_MINOR)
  README = open('./README.md', 'r')
  print(README.read())

# Load configuration file options into global variables
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

# Logs app state into log - I've learned recently that this way might be bad practice?
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

# Parameters used when executing script
def Parameters(argv):
  try:
    opts, args = getopt.getopt(argv,
                               "hdBLlGgs",["help","debug","bridge","lid-info","--lid","--gid-info","-git","--state"])
  except getopt.GetoptError:
    Help_Text()
    print('Invalid argument used')
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-h', '--help'): # Print help text and exit
      Help_Text()
      sys.exit(0)
    elif opt in ('-d', '--debug'): # Enter debug mode
      LOG_LEVEL = 1
      Log_Message (1, "Debug Logging enabled.")
    elif opt in ('-B', '--bridge'): # Return bridge information
      print('bridge')
    elif opt in ('-L', '--lid-info'): # Return Light(s) information
      print('lid-info')
    elif opt in ('-l', '--lid'): # Light(s) to modify
      print('lid')
    elif opt in ('-G', '--gid-info'): # Return Group(s) information
      print('gid-info')
    elif opt in ('-g', '--gid'): # Group(s) to modify
      print('gid')
    elif opt in ('-s', '--state'): # Change state of Light/Group
      print('state')

# Track tasks loaded into parameters


# Create AUTH_TOKEN variable used to communicate with API
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

# Validate API interaction was successful
def check_response(data):
  if bool(re.match('\[{"error":{', data)):
    json_error = json.loads(data)
    # Example error [{'error': {'type': 1, 'address': '/', 'description': 'unauthorized user'}}]
    Log_Message(4, str(json_error))
    sys.exit('Error Occurred')
    # Should add error handling - once I know what kind of errors can appear
  else:
    return True

#### #### Class Light
class Light:
  # When creating class object save all info into variables
  def __init__(self, lid, data):
    self.id = lid
    self.info = json.loads(json.dumps(data))
    #print('--- state ---')
    #print(self.info["state"])
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

#### #### Class Group #### ####
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

#### #### Class Bridge
class Bridge:
  # When creating class object pull data from bridge and save it into variables
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
    self.pull_lights()
    self.pull_groups()

  ### INFO PULLING FUNCTIONS
  # Pull info for all lights, save to a list, and crate light class object for each light
  def pull_lights(self):
    cmd = 'curl ' + AUTH_TOKEN + '/lights'
    data = os.popen(cmd).read().strip()
    check_response(data)
    lights = json.loads(data)
    for light in lights:
      #print('--- lights[light] ---')
      #print(lights[light])
      self.lights.append( Light( light, lights[light]) )
    #for obj in self.lights:
    #  print( obj.name, obj.id, obj.type )

  # Pull info for all groups, save to a list, and create group class object for each group
  def pull_groups(self):
    cmd = 'curl ' + AUTH_TOKEN + '/groups'
    data = os.popen(cmd).read().strip()
    check_response(data)
    groups = json.loads(data)
    for group in groups:
      #print(group)
      #print(groups[group])
      self.groups.append( Group( group, groups[group]) )
    #for obj in self.groups:
    #  print( obj.name, obj.id, obj.type )

  # Update Light/Group class object's info
  def update_info(self, obj):
    # Check if object is light or group
    if re.search(".*light", obj.type):
      # Pull and update class state variables
      cmd = 'curl ' + AUTH_TOKEN + '/lights/' + obj.id
      data = os.popen(cmd).read().strip()
      check_response(data)
      info = json.loads(data)
      obj.load_state(info["state"])
    else:
      # Pull and update class state/action variables
      cmd = 'curl ' + AUTH_TOKEN + '/groups/' + obj.id
      data = os.popen(cmd).read().strip()
      check_response(data)
      info = json.loads(data)
      obj.load_action(info["action"])
      obj.load_state(info["state"])

  ### STATE UPDATING FUNCTIONS
  # Toggle Light/Group on/off then update class object's info
  def toggle_on(self, obj):
    if obj.on == True:
      body = '\'{"on":false}\''
    elif obj.on == False:
      body = '\'{"on":true}\''
    if re.search(".*light", obj.type):
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/lights/' + str(obj.id) + '/state -d ' + body
    else:
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/groups/' + str(obj.id) + '/action -d ' + body
    response = os.popen(cmd).read().strip()
    check_response(response)
    self.update_info(obj)

  # Change Brightness (bri) for Light/Group
  # 0 to 255
  def update_bri(self, obj, value):
    body = '\'{"bri":' + str(value) + '}\''
    if re.search(".*light", obj.type):
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/lights/' + str(obj.id) + '/state -d ' + body
    else:
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/groups/' + str(obj.id) + '/action -d ' + body
    response = os.popen(cmd).read().strip()
    check_response(response)
    self.update_info(obj)

  # Change Hue for Light/Group
  # 0 to 65535
  def update_hue(self, obj, value):
    body = '\'{"hue":' + str(value) + '}\''
    if re.search(".*light", obj.type):
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/lights/' + str(obj.id) + '/state -d ' + body
    else:
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/groups/' + str(obj.id) + '/action -d ' + body
    response = os.popen(cmd).read().strip()
    check_response(response)
    self.update_info(obj)

  # Change Saturation (sat) for Light/Group
  # 0 to 255
  def update_sat(self, obj, value):
    body = '\'{"sat":' + str(value) + '}\''
    if re.search(".*light", obj.type):
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/lights/' + str(obj.id) + '/state -d ' + body
    else:
      cmd = 'curl -X PUT ' + AUTH_TOKEN + '/groups/' + str(obj.id) + '/action -d ' + body
    response = os.popen(cmd).read().strip()
    check_response(response)
    self.update_info(obj)

  # Change effect for Light/Group
  def update_effect(self, obj, value):
    pass
  # Change xy for Light/Group
  def update_xy(self, obj, value):
    pass
  # Change ct for Light/Group
  def update_ct(self, obj, value):
    pass
  # Change alert for Light/Group
  def update_alert(self, obj, value):
    pass
  # Change colormode for Light/Group
  def update_colormode(self, obj, value):
    pass

# Main Sequence
Parameters(sys.argv[1:])
Load_Conf()
Auth()
myBridge = Bridge()
