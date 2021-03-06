# argParser
# this class generates a RunParams object from the args passed to the script

from runparams import * 
import os.path
import string

## handles args passed to the program
#
class ArgParser(object):
	 
    def parsePtCutString(self, ptCutString):
	return map(float, string.split(ptCutString,',') )
    
    def parseEventsString(self, eventsString):
	return map(int, string.split(eventsString,',') )
	 
    def displayUserInfo(self):
	    print ""
	    print "o------------------o"
	    print "|Extracthistos Info|"
	    print "o------------------o"
	    print ""
	    print "[example usage]"
	    print ""
	    print "extracthistos inputFile.root"
	    print ""
	    print "extracthistos inputFile.root /intputDir/*.root --visualize --output outputfile-extracted.root --ptcuts 20,30,50,100 --etacut 2.5 --limit 100"
	    print ""
	    print "extracthistos inputFile.root /intputDir/*.root -v -o outputfile-extracted.root -p 20,30,50,100 -e 2.5 -l 100"
	    print ""
	    print "[switches]"
	    print " -d   | --debug:                          Show debug information"
	    print " -e   | --etacut:                         Set etaCut (double)"
	    print " -f   | --force:                          Force overwriting of output file"
	    print " -i   | --info:                           Shows this info"
	    print " -l   | --limit:                          Limit maximum # of events processed"
	    print " -o   | --output:                         Set output file (string)"
	    print " -od  | --output-outputdirectory:         Set output directory (string)"
	    print " -p   | --ptcuts:                         Set pTcuts (list of doubles seperated by ',')"
	    print " -#   | --events:                         Specify events to processed (list of ints seperated by ',')"
	    print " -m   | --multi-processing:               create n (int) subprocesses"
	    print " -%   | --modulo:                         process only every nth event (int)"
	    print " -%r  | --modulo-rest:                    process only every nth + r event (int)"
	    print " -v   | --visualize:                      Create visualization(s)"
	    print " -vs  | --visualize-skip-copies:          Do not render non-physical particle copies"
	    print " -vnu | --visualize-no-underlying-event:  Do not visualize the underlying event"
	    print " -vni | --visualize-no-main-interaction:  Do not visualize the main interaction"
	    print " -vsj | --visualize-color-special-jets:   Color special particle jets"
	    print " -vce | --visualize-cutoff-energy:        Specify Visualization energy cutoff (double)"
	    print " -vcs | --visualize-cutoff-special-jets:  Cutoff Special Jets"
	    print " -vcr | --visualize-cutoff-radiation:     Cutoff ISR/FSR Jets"
	    print " -vme | --visualize-mode-energy:          Color particles by their energy"
	    print " -vmp | --visualize-mode-pt:              Color particles by their pT"
	    print " -vr  | --visualize-renderer:             Specify GraphViz renderer (string), defaults to 'dot'"
	    print ""
	    
    def __init__(self, args):

	self.runParams = RunParams()
	
	lenArgs = len(args)
	
	skip = False
	forceOutputOverride = False
	
	for i in range (0, lenArgs):
		# skip first arg as it's the script's name
		if i == 0 or skip:
			skip = False
			continue
				
		# provide arg and nextArg (if possible)
		arg = args[i]
		nextArg = None
		if (i < lenArgs - 1):
			nextArg = args[i+1]
			
		# parse switches
	    	if ( arg == "-d" ) or ( arg == "--debug" )  :
		    self.runParams.useDebugOutput = True
		    continue
		if ( arg == "-e" ) or ( arg == "--etacut" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.eta = float(nextArg)
		    skip = True
		    continue
		if ( arg == "-f" ) or ( arg == "--force" )  :
		    forceOutputOverride = True
		    continue
		if ( arg == "-i" ) or ( arg == "--info" )  :
		    self.displayUserInfo()
		    self.runParams.run = False
		    break

		if ( arg == "-l" ) or ( arg == "--limit" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.maxEvents = int(nextArg)
		    skip = True
		    continue
	    	if ( arg == "-o" ) or ( arg == "--output" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    if nextArg [-15:] <> '-extracted.root':
			    raise Exception("'" + arg + "': Output file must end with '-extracted.root'!")
		    self.runParams.outputFile = nextArg
		    skip = True
		    continue
		if ( arg == "-p" ) or ( arg == "--ptcuts" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    ptCutString = nextArg
		    self.runParams.pTCuts = self.parsePtCutString(ptCutString)
		    skip = True
		    continue
		if ( arg == "-v" ) or ( arg == "--visualize" )  :
		    self.runParams.useVisualization = True
		    continue
		
		if ( arg == "-vs" ) or ( arg == "--visualize-skip-copies" )  :
		    self.runParams.visualizationSkipCopies = True
		    continue
		
		if ( arg == "-vnu" ) or ( arg == "--visualize-no-underlying-event" )  :
		    self.runParams.visualizationShowUnderlyingEvent = False
		    continue
		
		if ( arg == "-vni" ) or ( arg == "--visualize-no-main-interaction" )  :
		    self.runParams.visualizationShowMainInteraction = False
		    continue
		
		if ( arg == "-vsj" ) or ( arg == "--visualize-color-special-jets" )  :
		    self.runParams.visualizationColorSpecialJets = True
		    continue
		
		if ( arg == "-vme" ) or ( arg == "--visualize-mode-energy" )  :
		    self.runParams.visualizationEnergyMode = True
		    continue
		
		if ( arg == "-vmp" ) or ( arg == "--visualize-mode-pt" )  :
		    self.runParams.visualizationPtMode = True
		    continue
		
		if ( arg == "-vce" ) or ( arg == "--visualize-cutoff-energy" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.visualizationEnergyCutoff = int(nextArg)
		    skip = True
		    continue
		
		if ( arg == "-vcr" ) or ( arg == "--visualize-cutoff-radiation" )  :
		    self.runParams.visualizationCutoffRadiation = True
		    continue
		
		if ( arg == "-vcs" ) or ( arg == "--visualize-cutoff-special-jets" )  :
		    self.runParams.visualizationCutSpecialJets = True
		    continue
		
		#if ( arg == "-vp" ) or ( arg == "--visualize-pt-cutoff" )  :
		    #if nextArg is None or nextArg[0] == '-':
			     #raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    #self.runParams.visualizationPtCutoff = int(nextArg)
		    #skip = True
		    #continue
		
		if ( arg == "-vr" ) or ( arg == "--visualize-renderer:" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.visualizationRenderer = nextArg
		    skip = True
		    continue
		
		#if ( arg == "-z" ) or ( arg == "--zero-jets" )  :
		    #self.runParams.zeroAdditionalJets = True
		    #continue
		if ( arg == "-#" ) or ( arg == "--events" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    eventsString = nextArg
		    self.runParams.events = self.parseEventsString(eventsString)
		    skip = True
		    continue
				
	    	if ( arg == "-od" ) or ( arg == "--output-outputdirectory" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.outputDir = nextArg
		    skip = True
		    continue
		if ( arg == "-m" ) or ( arg == "--multi-processing" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.multiProcessing = int(nextArg)
		    skip = True
		    continue
		if ( arg == "-%" ) or ( arg == "--modulo" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.modulo = int(nextArg)
		    skip = True
		    continue
		if ( arg == "-%r" ) or ( arg == "--modulo-rest" )  :
		    if nextArg is None or nextArg[0] == '-':
			     raise Exception("'" + arg + "': Parse Error after '"+arg+"'!")
		    self.runParams.moduloRest = int(nextArg)
		    skip = True
		    continue
			
		if (arg[0] == '-'):
			raise Exception("'" + arg + "' is not a valid switch!")
		
		# deny input files ending with '-extracted.root', as this is our signature for output files:
		if arg[-15:] == '-extracted.root':
			print "Warning: File '" + arg + "' is being skipped."
			continue
		
		# parse input files:
		if arg[-5:] == '.root':
			thisFile = arg
			if thisFile[:7] == "/store/":
				if not os.path.isfile(thisFile):
					thisFile = "root://xrootd.ba.infn.it/" + thisFile
			else:
				if not os.path.isfile(thisFile):
					raise Exception("File '" + thisFile + "' does not exist!")
			self.runParams.inputFileList.append(thisFile)
			continue
		
		raise Exception("'" + arg + "' is not a valid root file!")
	
	if self.runParams.useVisualization and len(self.runParams.inputFileList) > 1:
		raise Exception("Visualization is allowed only for exactly one input file.")
		
	
	if self.runParams.run:
		if os.path.isfile(self.runParams.outputFile) and not forceOutputOverride:
			raise Exception("'" + self.runParams.outputFile + "' exists. Use the --force switch to force overriding.")
		
	if len(self.runParams.outputDir) <> 0:
		if not os.path.exists(self.runParams.outputDir):
			os.makedirs(self.runParams.outputDir)
		self.runParams.outputFilePath = self.runParams.outputDir + "/" + self.runParams.outputFile
	else:
		self.runParams.outputFilePath = self.runParams.outputFile
					
	#self.displayInfo()
