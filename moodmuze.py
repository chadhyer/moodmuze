#### Imported Packages
import getopt #parameters
import json #handle json data
import re #regular expression
from extra_utils import get_key_value_pair, read_file, log_message
from settings import *
from sys import exit
from hue import *


def parameters(argv):
  global task_lid
  global task_gid
  global task_dict
  try:
    opts, args = getopt.getopt(argv,"hdl:g:s:v:O:B:H:S:E:X:c:A:C:b:",
      ["help","debug","lid","state","value","on","bri","hue","sat",
      "effect","xy","ct","alert","colormode","body"])
  except getopt.GetoptError:
    read_file('README.md')
    sys.exit('Invalid argument!')
  for opt, arg in opts:
    if opt in ('-h', '--help'): # Print help text and exit
      read_file('README.md')
      sys.exit(0)
    elif opt in ('-d', '--debug'): # Enter debug mode
      LOG_LEVEL = 1
      log_message (1, "Debug logging enabled via parameter")
    elif opt in ('-l', '--lid'): # Light(s) to modify
      task_lid = arg
    elif opt in ('-g', '--gid'): # Group(s) to modify
      task_gid = arg
    elif opt in ('-O', '--on'):
      if arg == 'true' or arg == 'True':
        task_dict["on"] = True
      elif arg == 'false' or arg == 'False':
        task_dict["on"] = False
    elif opt in ('-B', '--bri'):
      task_dict["bri"] = int(arg)
    elif opt in ('-H', '--hue'):
      task_dict["hue"] = int(arg)
    elif opt in ('-S', '--sat'):
      task_dict["sat"] = int(arg)
    elif opt in ('-E', '--effect'):
      if arg != "none" and arg != "colorloop":
        sys.exit('Invalid option for -E --effect')
      task_dict["effect"] = str(arg)
    elif opt in ('-X', '--xy'):
      pass
    elif opt in ('-c', '--ct'):
      task_dict["ct"] = int(arg)
    elif opt in ('-A', '--alert'):
      task_dict["alert"] = str(arg)
    elif opt in ('-C', '--colormode'):
      task_dict["colormode"] = str(arg)

# Main Sequence
INFO = get_key_value_pair('moodmuze.info')
log_message(2, '--- Initiating ' + INFO["NAME"] + ' v' + INFO["MAJOR"] + '.'
            + INFO["MINOR"] + '.' + INFO["PATCH"] + '---' )
MyBridge = Bridge(BRIDGE_IP, AUTH_KEY, PROXY)
MyBridge.get_config()
