import sys, json, os, re, platform
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
if (base_dir is None) or (base_dir == "None"):
	exit(1)

file_sep="/"
if re.search(r'.*Windows.*', platform.system()):
	file_sep="\\"

base_dir = str(base_dir+file_sep)
if os.path.isdir(str(base_dir)):
	platforms = os.listdir(str(base_dir))
else:
	exit(1)

r1 = re.compile(".*windows.*")
platform_target = filter(r1.match, platforms)	
	
if platform_target:
	hosts = os.listdir(str(base_dir)+str(platform_target[0]))
else:
	exit(1)

if hosts:
	r2 = re.compile(".*consoles.*")
	for host in hosts:
		targets = os.listdir(str(base_dir)+str(platform_target[0])+file_sep+str(host))
		target = filter(r2.match, targets)
		if target:
			for fitem in target:
		#print "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format("host", "Console Process", "Console PID", "Console ID", "Command History Size", "History Buffer Count", "History Buffer Max", "OriginalTitle", "Title", "Attached Process Name", "Attached Process PID", "Attached Process Handle", "Command History ID", "Command History Applications", "Command History Flags", "Command History Count", "Command History Last Added", "Command History Last Displayed", "Command History First Command", "Command History Command Count Max", "Command History Process Handle", "Command History Command Number", "Command History Command Offset", "Command History Command String", "EXE Alias", "EXE Alias Source", "EXE Alias Target", "Screen ID", "Screen X", "Screen Y", "Screen Dump")
				with open(str(str(base_dir)+str(platform_target[0])+file_sep+str(host)+file_sep+fitem), 'r') as f:
					windows_consoles = None
					try:
						windows_consoles =  json.loads(f.readline())
					except:
						pass

					if windows_consoles:
						for element in windows_consoles['rows']:
							element	= [str(x) for x in element]
							element = [(re.sub(r'\\', r'\\\\', str(el))) for el in element]
							try:
								print host+"\t"+"\t".join(element)
							except:
								pass
				os.remove(str(str(base_dir)+str(platform_target[0])+file_sep+str(host)+file_sep+fitem))			
else:
	exit(1)
