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
        #get the type of var 1 is for string 2 is for float 3 is for int
        self.type = {}
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
        #use all the new code for the run
        self.get_run()


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
                    if not i.rstrip().endswith(">") and i.rstrip():
                        self.error(f"Error on line {self.line}. Reason: does not have > as the ending character")
                    else:
                        self.code[self.line] = i.rstrip()

    #get the types with a functiom
    def get_type(self,pass_in, line):
        pass_in = pass_in.strip()

        if "." in pass_in and pass_in.replace(".", "", 1).isdigit():
            return "float"
        elif pass_in.isdigit():
            return "int"
        elif (pass_in.startswith('"') and pass_in.endswith('"')) or (pass_in.startswith("'") and pass_in.endswith("'")):
            return "str"
        else:
            self.error(f"Error on line {line}. Reason: not supported type")

    #run the code
    def run(self, command, pass_in, name):
        if command == "say":
            print(pass_in) 
        elif command == "var":
            self.global_vars[name] = pass_in

    #go through the code so it can run
    def get_run(self):
        #the say function
        for i in sorted(self.code.keys()):
            if self.code[i].strip().startswith("say("):
                inside = self.code[i][self.code[i].index("say(") + 4 : self.code[i].rfind(")")]
                if inside.startswith('"') and inside.endswith('"'):
                    self.run("say", inside.strip('"'), None)
            #the vars
            elif self.code[i].strip().startswith("var"):
                name = self.code[i][self.code[i].index("var") + 3 : self.code[i].rfind("=")].strip()
                inside = self.code[i][self.code[i].index("=") + 1 : self.code[i].rfind(">")].strip()
                self.type[name] = self.get_type(inside, i)
                self.run("var", inside, name)
            #leave this as the last line so it can give the error right
            else:
                self.error(f"Error on line {i}. Reason: line did not have a indicator for a function that exists")

#I might make a tokenizer someday and a Parser

engine = language(filename)