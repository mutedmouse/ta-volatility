import sys, json, os, re, platform, itertools, importlib, TAtestplug

#Prechecks class whould only be instantiated one time to verify the presence of
# required folders and files necessary for successful operation
# The functions included perform those checks itteratively and exit with error
# code 1 if required elements are not found
# Additional logging and error identification will be included in subsequent releases
class preChecks:
	supported_platforms = ['windows', 'linux', 'mac']
	hosts = {}

	#This function gets the proper file separator for the hosting system
	# Linux, OSX and all others use / (no escaping required)
	# Windows uses \ (escaping required)
	def getFileSeperator(self, base_dir):
		if (base_dir is None) or (base_dir == "None"):
			#No base directory given to start with == bomb out
			 exit(1)

		#Define standard unix styp file separator
		file_sep="/"
		#Change to windows type double escaped file separator if windows splunk
		if re.search(r'.*Windows.*', platform.system()):
			#must use double \ due to python escape character treatment
			file_sep="\\"
		#send back identified file separator
		return file_sep

	#This function retrieves the available platforms in the base_dir folder
	# Example: __base_dir
	#		|_windows
	#		|_linux
	#
	# Return value would be [ 'windows', 'linux' ]
	def getPlatformFolders(self, base_dir):
		#validate that folder exist under base_dir
		if os.path.isdir(str(base_dir)):
			#return the list of folders under base_dir
			return os.listdir(str(base_dir))
		#handle instance with no folders under base_dir
		else:
			#bomb out if no folders are found under base_dir
			exit(1)

	#This function retrieves a list of hostname folders with platform
	# folders within base_dir
	# It maps the identified host folders in a dictionary with platform folders
	# as the key value
	# Example: __base_dir
	#		|_windows
	#		|   |_hostname1
	#		|   |_hostname3
	#		|_linux
	#		    |_hostname2
	#
	# Return value would be { 'windows': [ 'hostname1', 'hostname3' ],
	# 			  'linux': [ 'hostname2' ] }
	def getHostFolders(self, base_dir, platforms):
		# itterates through the identified supported_platforms list
		for arch in self.supported_platforms:
			#creates a basic regex pattern for faster filtering below
			pattern=re.compile(arch)
			#isolated matching platform folder within base_dir to current
			# supported_platform value from identified platforms
			platform_target = filter(pattern.match, platforms)
			#if a matching platform is found from the filter condition
			if platform_target:
				#if folders are found in matching platform condition
				if os.listdir(str(base_dir)+str(platform_target[0])):
					#assign list of folders found in matching
					# platform folder to hosts[arch] dictionary
					# key value
					self.hosts[arch] = os.listdir(str(base_dir)+str(platform_target[0]))

		#if hosts dictionary exists condition
		if self.hosts:
			#return the hosts dictionary for further processing	
			return self.hosts
		#no valid folders were found condition
		else:
			#bomb out if no valid folder were found for identified platforms
			exit(1)

#Parser class is the workhorse of the TA
#This class handles the remapping of the hosts and platforms to plugins
#It then loads only the plugins needed and del the variable after to conserve and 
# maximize memory efficiency
#It will attempt to handle ingest by plugin rather than by host folder
# In this way we can process, for example, all hosts containing a pslist output at
# one by one and then move onto the next plugin
#
#There are three functions to the parser class:
# getPossiblePlugins: which performs the identification of applicable json files from
# 		      the identified host folders
#
#		      This function also remaps the arch -> host -> plugin dictionary
#		      into an arch -> plugin -> hosts dictionary
#
# parser: which performs the import test of the plugin output file's class by name from
#	  TAplugin.py
#
#	  This is also the function that identifies whether a "custom" formatter is
#	  required by the plugin.  This can be controlled in the TAplugin and TAplugtest files
#
#
# format: which performs the standard remapping to key:value dictionary json format from the
#	  volatility unified_output format.
#
#	  It then prints this to the current termina screen (splunks scripted input) and deletes
#	  the original file to prevent repeat ingest of the same source data
#
#	  Future implementation is to move the successfully ingested file to a 'archive' folder
#	  within each host folder and rename the file to keep an epoch time track of when it was
#	  processed.  Example: archive -> 1526632902_pslist.json (formerly pslist.py)
class parser:
	#This function polls the host directories and gets any non-zero length, non-transferring
	# file with the json extension and loads it into a possible plugin list
	# It then maps each arch with its associated plugins and then finally to all the hosts that
	# plugin applies to
	# This is passed back to input for parsing calls
	def getPossiblePlugins(self, file_sep, base_dir, builderDict):
		#define blank dictionary
		archval = {}
		#define temp and filepart (incomplete transfers and writes) regex for faster filter
		noPart = re.compile("(?!.*\.(filepart|tmp)$)")
		#define regex pattern to only grab json file extensions
		jsonFiles = re.compile(".*\.json$")
		#itterate through for platform keys in passed dictionary
		for arch in builderDict.keys():
			#define architecture[arch] blank dictionary for population
			archval[arch]={}
			#itterate through hosts in passed dictionary that match arch value
			for host in builderDict[arch]:
				#define blank list for plugins by arch and hostname folders
				pluginList = []
				#create list of all .json files that do not match temp extensions
				# within the built path of base_dir[/|\\]arch[/|\\]hostname[/|\\]
				fileList = filter(jsonFiles.match, filter(noPart.match, os.listdir(base_dir+arch+file_sep+host)))
				#if the fileList variable is not None condition
				if fileList:
					#itterate through .json file identified in hostname folder
					for plugin in fileList:
						#check for zero length file condition
						if os.stat(str(base_dir+arch+file_sep+host+file_sep+plugin)).st_size != 0:
							#add non-zero, non-temp .json plugin to
							# to possible plugin list
							pluginList.append(plugin)
					#add complete plugin list for identified host to
					# host dictionary
					# Example: __base_dir
					#		|_windows
					#		|   |_hostname1
					#		|   |	|_plugin1.json
					#		|   |	|_plugin5.json
					#		|   |_hostname3
					#		|   |	|_plugin1.json
					#		|   |	|_plugin4.json
					#		|_linux
					#		    |_hostname2
					#		    	|_plugin2.json
					#	ignored ------->|_plugin3.json.filepart
					#	ignored ------->|_plugin6.json.tmp
					#	ignored ------->|_plugin7.json (zero-length)
					#
					# Resultant dictionary would be: 
					# { 'windows': 
					#	{ 'hostname1':
					#		[ 'plugin1.json', 'plugin5.json' ] },
					#	{ 'hostname3':
					#		[ 'plugin1.json', 'plugin4.json' ] },
					#   'linux':
					#	{ 'hostname2':
					#		[ 'plugin2.json'] },
					# }
					archval[arch][host] = pluginList

		#itterate through platforms in newly built arval dictionary
		for arch in archval.keys():
			#remove all stored values for arch dictionary in buiderDict
			# this is done in preparation to load new tuples
			builderDict[arch]={}
			#itterate through list of unique plugins by name from archval dict
			for plugin in list(set(list(itertools.chain.from_iterable(archval[arch].values())))):
				#perform list comprehension per plugin to identify applicable hosts
				#Equivalent expansion code:
				# hosts = []
				# for host in archval[arch].keys():
				#	if plugin in archval[arch][host]
				#		hosts.append(host)
				hosts = [ host for host in archval[arch].keys() if plugin in archval[arch][host] ]
				#regular expression to remove .json extension from plugin string
				plugin=re.sub("\.json", "", plugin)
				#assign new list of hosts to builderDict's arch's plugin key
				# Example: 
				# Original builderDict dictionary: 
				# { 'windows': 
				#	{ 'hostname1':
				#		[ 'plugin1.json', 'plugin5.json' ] },
				#	{ 'hostname3':
				#		[ 'plugin1.json', 'plugin4.json' ] },
				#   'linux':
				#	{ 'hostname2':
				#		[ 'plugin2.json'] },
				# }
				#
				# Resultant builderDict dictionary: 
				# { 'windows': 
				#	{ 'plugin1':
				#		[ 'hostname1', 'hostname3' ] },
				#	{ 'plugin5':
				#		[ 'hostname1' ] },
				#	{ 'plugin4':
				#		[ 'hostname3' ] },
				#   'linux':
				#	{ 'plugin2':
				#		[ 'hostname2'] },
				# }
				builderDict[arch][plugin]=hosts

		#return dictionary to input for parsing
		return builderDict

	#This function itterated by architecture by plugin
	# it then checks imported TAtestplug classes to verify plugin by string
	# next it looks at the mode variable of the imported and instantiated class
	# if the mode is "standard" this function will call the local 'format' function
	# if the mode is anything else it will attempt to load imported plugin's class 'format'
	#  function
	# following all operations it will move through the plugins until it finishes all
	#  all plugins
	# upon platform completion it will move to the next listed platform and walk the
	#  plugins for that platform
	# the application exits after this function is complete	
	def parse(self, file_sep, base_dir, builderDict):
		#prepare import of TAtestplug.py classes
		pluginmodule = importlib.import_module('TAtestplug')
		#itterate through platforms in top level of builderDict
		# potential values of [ 'windows', 'linux', 'mac' ]
		# hold value of each itteration in variable arch
		for arch in builderDict.keys():
			#itterate through each unique potential plugin in each arch
			# potential values are any file with .json extension from hostname folders
			for plugin in builderDict[arch].keys():
				#reset pluginClass variable per plugin itteration
				pluginClass = None				
				#Reset instance variable per plugin itteration
				instance = None
				#This try/except block attempts to load the plugin class from
				#TAtestplug via the pluginmodule that loaded the module earlier
				#
				#We pass the exception because the variable is tested for blank
				# values in the subsequent conditional evaulation below
				#
				#Subsequent releases incorporating error logging will log these
				# error for troubleshooting and development assistance
				#
				#This must be a try/except block because failure to handle this
				# exception will cause the entire input.py script to halt and exit
				try:
					#Attempt to load the class (from string variable plugin)
					# into parsingClass instance
					#
					#This will drop an attribute error of NoneType or no
					# such class in the event the class is not defined in
					# TAtestplug.py
					parsingClass = getattr(pluginmodule, plugin)
					#Attempt to initialize variable of parsingClass()
					instance = parsingClass()
				#catch attribute error exceptions thrown from nonexistent plugins
				except AttributeError:
					#Dump the exception as it is tested in the next condition
					#
					#Future release: log this error with plugin name to error
					# log file within app
					pass

				#test for valid instance variable codition
				if instance:
					#reset pparser vairable in case we need to load custom
					# format and plugin function
					parser=None
					#Test instance parsing mode variable value
					# only value we care about is "standard"
					#
					#If using custom formatting in TAtestplug.py please
					# set the value of your plugin class ' variable mode
					# to something else other than "standard"
					if instance.mode == "standard":
						#itterate through host list within plugin key value
						for host in builderDict[arch][plugin]:
							#since instance.mode is "standard"
							# we will use out self.format function
							#
							#This format function is defined following
							# the closure of current function
							self.format(file_sep,base_dir, arch, plugin, host)
					#instance.mode!="standard" condition
					#this is the custom stuff, rare but available if required
					else:
						#verify existence of 'format' method within plugin
						# class definition
						if getattr(instance, "format", None):
							#itterate through host list within plugin
							# key value
							for host in builderDict[arch][plugin]:
								#call instances' version of format
								# method instead of our own local
								# version
								instance.format(file_sep,base_dir, arch, plugin, host)
					#remove the variable parser from memory (garbage collector)
					del parser
				#remove the variable instance from memory (garbage collector)
				del instance

	#This function simply remaps the JSON dictionary from the plugin output file to make the
	# 'columns' values into the keys for each of the rows value
	#
	#Example:
	# Original JSON dictionary from volatility:
	#	{"rows": [[2164987488, "System", 4, 0, 61, 179, -1, 0, "", ""], 
	#		  [4280987680, "smss.exe", 544, 4, 3, 21, -1, 0, "2010-08-11 06:06:21 UTC+0000", ""]],
	#	 "columns": ["Offset(V)", "Name", "PID", "PPID", "Thds", "Hnds", "Sess", "Wow64", "Start", "Exit"]
	#	}
	# Resultant JSON dictionary from volatility:
	#	{ "offsetv": "2164987488", 
	#	  "name": "System", 
	#	  "pid": "4", 
	#	  "ppid": "0",
	#	  "thds": "61",
	#	  "hnds": "179",
	#	  "sess": "-1",
	#	  "wow64": "0",
	#	  "start": "",
	#	  "orig_tuple": "hostname1_plugin",
	#	  "platform": "windows",
	#	  "plugin": "plugin_name",
	#	  "stop": "" }, 
	#	{ "offsetv": "4280987680", 
	#	  "name": "System", 
	#	  "pid": "544", 
	#	  "ppid": "4",
	#	  "thds": "3",
	#	  "hnds": "21",
	#	  "sess": "-1",
	#	  "wow64": "0",
	#	  "start": "2010-08-11 06:06:21 UTC+0000",
	#	  "orig_tuple": "hostname1_plugin",
	#	  "platform": "windows",
	#	  "plugin": "plugin_name",
	#	  "stop": "" } 
	def format(self, file_sep, base_dir, arch, plugin, host):
		#Set the container to None
		container = None
		#Open the target plugin file within the platform and host folder
		with open(str(base_dir+arch+file_sep+host+file_sep+plugin+".json"), 'r') as f:
			#Must handle this with a try/except due to application breakage on
			# exception
			#
			#This exception block attempts to load the data from the json file as
			# json.loads
			#
			#Exceptions are not handled due to testing of value in subsequent
			# contidional statement
			try:
				#Attempt to load f (plugin file)
				container = json.loads(f.readline())
			#Catch the exceptions
			except:
				#Dump the exception
				#
				#Subsequent release will write these errors to log file within app
				pass

		#Test the container variable for successful json load condition
		if container:
			#Create blank temp dictionary to hold row values
			temp={}
			#Itterate through json "rows" values
			for element in container['rows']:
				#Add the plugin to the dictionary
				temp['plugin']=plugin
				#Add the architecture of the analysis to the dictionary
				temp['platform']=arch
				#Add the current hostname to the dictionary
				temp['image']=host
				#Add tuple of hostname_plugin.json to be used as source tag in
				# props.conf
				temp['orig_tuple']=str(host+"_"+plugin+".json")
				#Itterate through columns values using indices instead of values
				#By using indices we can map column indices to row lists' indeces
				#Example
				#	
				#Truncated JSON dictionary from volatility with index notation
				# below:
				#	{"rows": [[2164987488, "System", 4, 0, 61 ]],
				#			0	   1	 2  3   4 
				#	 "columns": ["Offset(V)", "Name", "PID", "PPID", "Thds"] }
				#			0	     1	    2	   3	   4
				#Variable col will hold the index values
				for col in range(len(container['columns'])):
					#This regex substitution removes "troublesome" characters
					# from the column names and lowercases the column names
					column=re.sub(r'[\(|_|\)]','', str(container['columns'][col].lower()))
					#This regex replaces backslashes with double backslashes
					#
					#Splunk display will convert \n for example into new lines
					#To permit splunk display we turn this into \\n here
				        temp[column]=re.sub(r'\\',r'\\\\', str(element[col]))
				#Print the entire temp dictionary to the screen (splunk tty really)
				print json.dumps(temp)
				#Reset the temp dictionary for the next row
				temp={}
			#File deletion is commented out for this test class
			#os.remove(str(base_dir+arch+file_sep+host+file_sep+plugin+".json"))
