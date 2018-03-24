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
	r2 = re.compile(".*deskscan.*")
	for host in hosts:
		targets = os.listdir(str(base_dir)+str(platform_target[0])+file_sep+str(host))
		target = filter(r2.match, targets)
		if target:
			for fitem in target:
		#print "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format("host", "Offset", "Name", "Next", "SessionId", "DesktopInfo", "fsHooks", "spwnd", "Windows", "Heap", "Size", "Base", "Limit", "ThreadId", "Process", "PID", "PPID")
				with open(str(str(base_dir)+str(platform_target[0])+file_sep+str(host)+file_sep+fitem), 'r') as f:
					windows_deskscan = None
					try:
						windows_deskscan =  json.loads(f.readline())
					except:
						pass


					if windows_deskscan:
						for element in windows_deskscan['rows']:
							element	= [str(x) for x in element]
							element = [(re.sub(r'\\', r'\\\\', str(el))) for el in element]
							try:
								print host+"\t"+"\t".join(element)
							except:
								pass
				os.remove(str(str(base_dir)+str(platform_target[0])+file_sep+str(host)+file_sep+fitem))			
else:
	exit(1)
