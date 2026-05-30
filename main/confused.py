import sys

#get the filename
filename = sys.argv[1]

# Source - https://stackoverflow.com/a/287944
# Posted by joeld, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-29, License - CC BY-SA 4.0
#the colors for errors
class colors:
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    under = '\033[4m'

#the interpreter for confused
class language:

    #the __init__ for the interpreter
    def __init__(self, file):
        #the lines of code
        self.code = {}
        #the mem for the global vars
        self.global_vars = {}
        #the filename
        self.filename = file
        #the line we are on
        self.line = 0
        self.gtgc = False #this means good to get code
        #read the file for the code
        self.allow_file()
        #get the code
        self.get_code()

    #make an error function to reuse this function prints the message and exits the code
    def error(self, message):
        print(colors.fail, colors.under + message + colors.endc)
        sys.exit(1)

    def allow_file(self):
        if not self.filename.endswith(".cfdy"):
            #tell the user that they don't haven the right file extension
            self.error("The file you are trying to run must have the file extension .cfdy")
        elif self.filename.endswith(".cfdy"):
            #set gtgc to true so we know to read the file
            self.gtgc = True
    
    #the function that is going to read the lines of code and store them for later use
    def get_code(self):
        if self.gtgc:
            #open the file and read the ai model told me to use this encoding
            with open(self.filename, "r", encoding="utf-8") as f:
                for i in f:
                    self.line += 1
                    self.code[self.line] = i.rstrip()

engine = language(filename)