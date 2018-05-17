import sys, json, os, re, platform, itertools, importlib, TAtestplug

class preChecks:
	supported_platforms = ['windows', 'linux', 'mac']
	hosts = {}

	def getFileSeperator(self, base_dir):
		if (base_dir is None) or (base_dir == "None"):
			#No base directory given to start with == bomb out
			 exit(1)

		file_sep="/"
		if re.search(r'.*Windows.*', platform.system()):
			file_sep="\\"
		return file_sep

	def getPlatformFolders(self, base_dir):
		if os.path.isdir(str(base_dir)):
			return os.listdir(str(base_dir))
		else:
			exit(1)

	def getHostFolders(self, base_dir, platforms):
		for arch in self.supported_platforms:
			pattern=re.compile(arch)
			platform_target = filter(pattern.match, platforms)
			if platform_target:
				if os.listdir(str(base_dir)+str(platform_target[0])):
					self.hosts[arch] = os.listdir(str(base_dir)+str(platform_target[0]))
					
		return self.hosts

class parser:
	def getPossiblePlugins(self, file_sep, base_dir, builderDict):
		archval = {}
		noPart = re.compile("(?!.*\.(filepart|tmp)$)")		
		for arch in builderDict.keys():
			archval[arch]={}
			for host in builderDict[arch]:
				pluginList = []
				fileList = filter(noPart.match, os.listdir(base_dir+arch+file_sep+host))
				if fileList:
					for plugin in fileList:
						if os.stat(str(base_dir+arch+file_sep+host+file_sep+plugin)).st_size != 0:
							pluginList.append(plugin)	
					archval[arch][host] = pluginList

		for arch in archval.keys():
			builderDict[arch]={}
			for plugin in list(set(list(itertools.chain.from_iterable(archval[arch].values())))):
				hosts = [ host for host in archval[arch].keys() if plugin in archval[arch][host] ]
				plugin=re.sub("\.json", "", plugin)
				builderDict[arch][plugin]=hosts
				#print plugin+",".join(hosts)

		return builderDict

		
	def parse(self, file_sep, base_dir, builderDict):
		pluginmodule = importlib.import_module('TAplugins')
		volmodule = importlib.import_module('TAvol')
		pluginClass = None
		for arch in builderDict.keys():
			for plugin in builderDict[arch].keys():
				instance = None
				try:
					pluginmodule = importlib.import_module('TAplugins')
					parsingClass = getattr(pluginmodule, plugin)
					instance = parsingClass()
				except AttributeError:
					pass

				if instance:
					parser=None
					if instance.mode == "standard":
						parsingMode = getattr(volmodule, "formatter")
						parser = parsingMode()
						for host in builderDict[arch][plugin]:
							parser.format(file_sep,base_dir, arch, plugin, host)
					else:
						parsingMode = getattr(pluginmodule, plugin)
						parser = parsingMode()
						parser.format()
					del parser
				del instance


class formatter:
	def format(self, file_sep, base_dir, arch, plugin, host):
		container = None
		with open(str(base_dir+arch+file_sep+host+file_sep+plugin+".json"), 'r') as f:
			try:
				container = json.loads(f.readline())
			except:
				pass

		if container:
			temp={}
			for element in container['rows']:
				temp['plugin']=plugin
				temp['platform']=arch
				temp['image']=host
				temp['orig_tuple']=str(host+"_"+plugin+".json")
				for col in range(len(container['columns'])):
					column=re.sub(r'[\(|_|\)]','', str(container['columns'][col].lower()))
				        temp[column]=re.sub(r'\\',r'\\\\', str(element[col]))
				print json.dumps(temp)
				temp={}
			#File removal has been commented out for testing class
			#os.remove(str(base_dir+arch+file_sep+host+file_sep+plugin+".json"))

