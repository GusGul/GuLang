from sys import *

tokens = []
key_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
key_operations = ["+", "-", "*", "/", "(", ")"]

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>"
    return data
    
def lexer(filecontents):
    filecontents = list(filecontents)
    
    # state = 0 means reading a command, state = 1 means reading a value
    state = 0
    isexpr = 0
    tok = ""
    string = ""
    expr = ""
    n = ""
    
    for char in filecontents:
        tok += char
        if tok == " ":
            if state == 0:
                tok = ""
            else:
                tok = " "
        elif tok == "\n" or tok == "" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
                tokens.append("EXPR:" + expr)
                expr = ""
            if expr != "" and isexpr == 0:
                tokens.append("NUM:" + expr)
                expr = ""
            tok = ""
        elif tok == "PRINT" or tok == "print":
            tokens.append("PRINT")
            tok = ""
        elif tok in key_numbers:
            expr += tok
            tok = ""
        elif tok in key_operations:
            isexpr = 1
            expr += tok
            tok = ""
        elif tok == "\"":
            if state == 0:
                state = 1
            elif state == 1:
                tokens.append("STRING:" + string + "\"")
                tok = ""
                string = ""
                state = 0
        elif state == 1:
            string += tok
            tok = ""
    #print(tokens)
    return tokens

def doPRINT(toPRINT):
    if toPRINT[0:6] == "STRING:":
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif toPRINT[0:3] == "NUM:":
        toPRINT = toPRINT[4:]
    elif toPRINT[0:4] == "EXPR:" :
        toPRINT = eval(toPRINT[5:])
    print(toPRINT)
                
def parse(toks):
    i = 0
    while(i < len(toks)):
        if toks[i] + " " + toks[i+1][0:6] == "PRINT STRING" or toks[i] + " " + toks[i+1][0:3] == "PRINT NUM" or toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR":
            if toks[i+1][0:6] == "STRING":
                doPRINT(toks[i+1])
            if toks[i+1][0:3] == "NUM":
                doPRINT(toks[i+1])
            if toks[i+1][0:4] == "EXPR":
                doPRINT(toks[i+1])
            i += 2

def run():
    data = open_file(argv[1])
    toks = lexer(data)
    parse(toks)
    
run()