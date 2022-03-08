#!/usr/bin/env python3

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

#### Imported Packages ####
import os #run os commands
import configparser #config file
import datetime #for datetime in log entries
import sys #exit
import getopt #parameters
import json #handle json data

#### Help_Text ####
def Help_Text():
  print( SELF_NAME + ' V' + SELF_MAJOR + '.' + SELF_MINOR + ' Help Text placeholder')

#### Load_Conf ####
def Load_Conf():
  global LOG_FILE
  global LOG_LEVEL
  global BRIDGE_IP
  global AUTH_FILE
  conf_exists = os.exists(SELF_CONF)
  if conf_exists != True:
    dt = datetime.datetime.now()
    sys.exit(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [ERROR]    Unable to find config file: ' + SELF_CONF + '! Exiting!!!'
  # Load Configuration Options
  LOG_FILE = config.get('Log', 'LOG_FILE')
  LOG_LEVEL = config.get('Log', 'LOG_LEVEL')
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
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + message, file = log)
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + message)
  elif level >= LOG_LEVEL:
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + message, file = log)
    print(dt.strftime("%Y-%m-%d %H:%M:%S") + '    [' + label + ']    ' + message)
  log.close()

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

#### ==== Main Sequence ==== ####

