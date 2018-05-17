import sys, json, os, re, platform, TAvol
from splunk.clilib import cli_common as cli

def GetBaseDirectory():
        appdir = os.path.dirname(os.path.dirname(__file__))
        localconfpath = os.path.join(appdir, "local", "vol.conf")
        conf = {}
        if os.path.exists(localconfpath):
                localconf = cli.readConfFile(localconfpath)
                for name, content in localconf.items():
                        if name == "configs":
                                return content['base_directory']

platforms = []
platform_target = []
hosts = []
target = []
base_dir = GetBaseDirectory().strip('"')
#base_dir = "/data/memory"

#instantiate arch class from TAvol relative import
validation=TAvol.preChecks()

#grab the file seperator for proper directory traversal
file_sep=validation.getFileSeperator(base_dir)

#Solidify base directory for later with file seperator included
#NOTE: Linux //data//memory is the same as /data/memory so this is a safety mechanism
#      Windows C:\\ translate to C:\ due to the escape slash usage
#      OSX is the same as linux / interpretation
base_dir = str(base_dir+file_sep)

#verify base directory exists and check for windows, linux or mac folders in base_dir
platforms = validation.getPlatformFolders(base_dir)

#build dictionary of supported hosts so we only load architectures (windows, linux, mac) we need
hosts = validation.getHostFolders(base_dir, platforms)

#id the plugins possible by file we will need to load based on the files we see in the hosts
# this function will return a dictionary that resembles the following:
## { 'windows': 
#              { 'plugin1': ['host1', 'host2' ],
#                'plugin2': ['host3', 'host2' ]
#              },
#    'linux' :
#              { 'plugin3': ['host10', 'host12' ],
#                'plugin4': ['host13', 'host12' ]
#              },
#    'mac' :
#              { 'plugin13': ['host11', 'host15' ],
#                'plugin14': ['host16', 'host17' ]
#              },
## )
# when we start loading plugins we will now be able to parse ALL files matching pluginX and then unload the class
# a dramatic efficiency should result by only loading what we need and destroying the class afterwards
parser = TAvol.parser()
pluginList = parser.getPossiblePlugins(file_sep, base_dir, hosts)
parser.parse(file_sep, base_dir, pluginList)
exit(0)
