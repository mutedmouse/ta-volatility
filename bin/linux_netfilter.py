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

r1 = re.compile(".*linux.*")
platform_target = filter(r1.match, platforms)	
	
if platform_target:
	hosts = os.listdir(str(base_dir)+str(platform_target[0]))
else:
	exit(1)

if hosts:
	r2 = re.compile(".*linux_netfilter.*")
	for host in hosts:
		targets = os.listdir(str(base_dir)+str(platform_target[0])+file_sep+str(host))
		target = filter(r2.match, targets)
		if target:
			for fitem in target:
		#print "{}\t{}\t{}\t{}".format("Proto", "Hook", "Handler", "IsHooked")
				with open(str(str(base_dir)+str(platform_target[0])+file_sep+str(host)+file_sep+fitem), 'r') as f:
					linux_netfilter = None
					try:
						linux_netfilter =  json.loads(f.readline())
					except:
						pass
					
					if linux_netfilter:
						for element in linux_netfilter['rows']:
							element = [str(x) for x in element]
							element = [(re.sub(r'\\', r'\\\\', str(el))) for el in element]
							try:
								print host+"\t"+"\t".join(element)
							except:
								pass
				os.remove(str(str(base_dir)+str(platform_target[0])+file_sep+str(host)+file_sep+fitem))			
else:
	exit(1)