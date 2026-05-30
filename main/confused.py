import sys

#get the filename
filename = sys.argv[1]

#the colors for errors
class colors:
    fail = '\033[91m'
    endc = '\033[0m'
    bold = '\033[1m'
    under = '\033[4m'

#the interpreter for confused
class interpreter:

    #the __init__ for the interpreter
    def __init__(self, file):
        self.global_vars = {}
        self.filename = file
        self.line = 0
        self.gtgc = False #this means good to get code
        #read the file for the code
        self.read_file()
    
    # Source - https://stackoverflow.com/a/287944
    # Posted by joeld, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-05-29, License - CC BY-SA 4.0

    def read_file(self):
        if not self.filename.endswith(".cfdy"):
            print(f"{colors.fail} {colors.under}The file you are trying to run must have the file extension .cfdy{colors.endc}")
            sys.exit(1)
        elif self.filename.endswith(".cfdy"):
            self.gtgc = True

engine = interpreter(filename)s