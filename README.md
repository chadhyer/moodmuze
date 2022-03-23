```
'##################################################################################################################'
'      ___           ___           ___          _____           ___           ___           ___           ___      '
'     /__/\         /  /\         /  /\        /  /::\         /\__\         /\__\         /\  \         /\  \     '
'    |  |::\       /  /::\       /  /::\      /  /:/\:\       /::|  |       /:/  /         \:\  \       /::\  \    '
'    |  |:|:\     /  /:/\:\     /  /:/\:\    /  /:/  \:\     /:|:|  |      /:/  /           \:\  \     /:/\:\  \   '
'  __|__|:|\:\   /  /:/  \:\   /  /:/  \:\  /__/:/ \__\:|   /:/|:|__|__   /:/  /  ___        \:\  \   /::\~\:\  \  '
' /__/::::| \:\ /__/:/ \__\:\ /__/:/ \__\:\ \  \:\ /  /:/  /:/ |::::\__\ /:/__/  /\__\ _______\:\__\ /:/\:\ \:\__\ '
' \  \:\~~\__\/ \  \:\ /  /:/ \  \:\ /  /:/  \  \:\  /:/   \/__/~~/:/  / \:\  \ /:/  / \::::::::/__/ \:\~\:\ \/__/ '
'  \  \:\        \  \:\  /:/   \  \:\  /:/    \  \:\/:/          /:/  /   \:\  /:/  /   \:\~~\~~      \:\ \:\__\   '
'   \  \:\        \  \:\/:/     \  \:\/:/      \  \::/          /:/  /     \:\/:/  /     \:\  \        \:\ \/__/   '
'    \  \:\        \  \::/       \  \::/        \__\/          /:/  /       \::/  /       \:\__\        \:\__\     '
'     \__\/         \__\/         \__\/                        \/__/         \/__/         \/__/         \/__/     '
'                                                                                                                  '
'##################################################################################################################'

Moodmuze

Parameters
----------
 -h --help             Print this help text
 -d --debug            Print debug lines
 -l --lid              ID of light to control
 -g --gid              ID of group to control
 -O --on <arg>         Power status to apply to object where <arg> is true to power on and false to power off
 -B --bri <arg>        Brightness level to apply to object where <arg> is int between 0 and 255
 -H --hue <arg>        Hue to apply to object where <arg> is int between 1 and 10000
 -S --sat <arg>        Saturation to apply to object where <arg> is int between 0 and 255
 -E --effect <arg>     Effect to apply to object where <arg> is none or colorloop
 -X --xy <arg>         XY of object. This has not been coded yet...
 -c --ct <arg>         Color tempature to apply to object where <arg> is int between 0 and 255
                       Object must be in colormode ct.
 -A --alert <arg>      Alert to apply to object where <arg> is none, select for 1 flash, and 
                       lselect for 15 seconds of flahing
 -C --colormode <arg>  Colormode to apply to object where <arg> is ...
 -b --body <arg>       This is not coded yet, but will allow formatted json body to be entered

moodmuse
Control your Philips Hue Bridge with API calls from this Python application
```
