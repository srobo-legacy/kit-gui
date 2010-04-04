p = -4
i = -5
d = -10

def getPidI ():
    global i
    return i

def setPidI (value):
    global i
    i = value
    
def getPidP ():
    global p
    return p

def setPidP (value):
    global p
    p = value

def getPidD ():
    global d
    return d

def setPidD (value):
    global d
    d = value

def pythonValidate():
    return True

def motorBoardConnected():
    return True

checks = [("Code Check", pythonValidate), ("Motor Board Connected", motorBoardConnected)]

