#!/usr/bin/env python3
#this is know as alpha 1.02
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
        #a list of functions to go through
        self.funcs_def = {
            "say": "says the thing that is passed into it and prints it to the console", 
            "var": "makes a var with a type and the data that goes with the var"
        }
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
    def error(self, message, code):
        if not code is None:
            print(f" {colors.fail}{ colors.under}This is the line that crashed: {code}{colors.endc}")
        print(colors.fail, colors.under + message + colors.endc)
        sys.exit(1)

    def allow_file(self):
        if not self.filename.endswith(".cfdy"):
            #tell the user that they don't haven the right file extension
            self.error("The file you are trying to run must have the file extension .cfdy", None)
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
                    #the comments for the language
                    if i.strip().startswith("#") or i.strip() == "":
                        self.code[self.line] = ">"
                    #the error for not having a > at the end
                    elif not i.rstrip().endswith(">") and i.rstrip():
                        self.error(f"Error on line {self.line}. Reason: does not have > as the ending character", i)
                    #adding the code
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
            self.error(f"Error on line {line}. Reason: not supported type", None)

    #run the code
    def run(self, command, pass_in, name):
        if command == "say":
            print(pass_in) 
        elif command == "var":
            self.global_vars[name.strip()] = pass_in
    
    #make a say function
    def say(self, inside):
        #the checks to see if it is a str or a int or a float
        if (inside.startswith('"') and inside.endswith('"')) or (inside.startswith("'") and inside.endswith("'")):
            #we are making a inside2 var so we can strip down inside of the things that make it a str
            inside2 = inside.strip('"').strip("'")
            self.run("say", inside2, None)
        elif inside.strip(".").isdigit():
            self.run("say", inside.strip(), None)
        elif inside in self.global_vars and inside in self.type:
            #we are making a inside2 var so we can strip down inside of the things that make it a str so it does not show up it the say
            var_val = self.global_vars[inside].strip()
            if (var_val.startswith("'") and var_val.endswith("'")) or (var_val.startswith('"') and var_val.endswith('"')):
                inside2 = var_val.strip("'").strip('"')
            else:
                inside2 = var_val    
            self.run("say", inside2, None)
            #something to find functions
        else:
            if inside.startswith("say(") and inside.endswith(")"):
                inside2 = inside[inside.index("say(") + 4 : inside.rfind(")")].strip()
                self.say(inside2)
    
    #the var function
    def var(self, line):
        name = self.code[line][self.code[line].index("var") + 3 : self.code[line].rfind("=")].strip()
        inside = self.code[line][self.code[line].index("=") + 1 : self.code[line].rfind(">")].strip()
        self.type[name.strip()] = self.get_type(inside, line)
        self.run("var", inside, name)

    #go through the code so it can run
    def get_run(self):  
        #the call for the say function
        for i in sorted(self.code.keys()):
            if self.code[i].strip().startswith("say("):
                #the inside of the say
                inside = self.code[i][self.code[i].index("say(") + 4 : self.code[i].rfind(")")]
                self.say(inside)
            #the call for the vars function
            elif self.code[i].strip().startswith("var"):
                self.var(i)
            #leave this as the last line so it can give the error right
            else:
                if self.code[i].strip() and (not self.code[i].startswith('>')):
                    self.error(f"Error on line {i}. Reason: line did not have a indicator for a function that exists", self.code[i])

#I might make a tokenizer someday and a Parser

engine = language(filename)