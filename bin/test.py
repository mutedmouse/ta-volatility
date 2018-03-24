import os
import sys
from splunk.clilib import cli_common as cli
 
def GetBaseDirectory():
	appdir = os.path.dirname(os.path.dirname(__file__))
	localconfpath = os.path.join(appdir, "local", "vol.conf")
	conf = {}
	if os.path.exists(localconfpath):
		localconf = cli.readConfFile(localconfpath)
		for name, content in localconf.items():
			if name == "configs":
				print content['base_directory']
		

GetBaseDirectory()
        

