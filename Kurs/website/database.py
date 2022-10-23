import re, os, datetime, hashlib, pickle, sys
from website import modules

userDatabasePath = os.getcwd()+"/data/userDatabase/Users/"
userDatabaseFilePath = os.getcwd()+"/data/userDatabase/userdatabase.db"
userPattern = re.compile("username:(.*)?;password:(.*)?;id:(.*)")
cookiePattern = re.compile("username:(.*)?;password:(.*)")

userList = []

def Run(_command):
    if _command == "":
        _command = input("Enter command: ")
    if _command == "-delU":
        #DeleteUser()
        return

def InitDB():
    #LoadUserObjects()
    LoadUsers()
    PrintDatabase()

def LoadUserObjects():
    global userList
    fileList = os.listdir(userDatabasePath)
    for file in fileList:
        userList.append(LoadUserObject(file))

def LoadUsers():
    global userList
    userdatabaseFile = open(userDatabaseFilePath, "r")
    lines = userdatabaseFile.readlines()
    for line in lines:
        userList.append(LoadUser(line))

def CreateUser(_username, _password):
    user = modules.User()
    user.username = _username
    user.password = _password
    user.id = CreateRandomId()
    SaveUser(user)
    SaveUserObject(user)
    global userList
    userList.append(user)
    return user

def SaveUser(_user):
    line = f"username:{_user.username};password:{_user.password};id:{_user.id}"
    userDatabaseFile = open(userDatabaseFilePath, "a")
    userDatabaseFile.writelines(line+"\n")
    userDatabaseFile.close()

def SaveUserObject(_userObject):
    userObjectFile = open(userDatabasePath+_userObject.id, "wb")
    pickle.dump(_userObject, userObjectFile)
    userObjectFile.close()

def LoadUser(_line):
    user = modules.User()
    result = re.search(userPattern, _line)
    user.username = result.group(1)
    user.password = result.group(2)
    user.id = result.group(3)
    return user

def LoadUserObject(_id):
    userObjectFile = open(userDatabasePath+_id, "rb")
    user = pickle.load(userObjectFile)
    userObjectFile.close()
    return user

def GetUserByUsername(_username):
    global userList
    for user in userList:
        if user.username == _username:
            return user
    return "invalid"

def GetUserById(_id):
    global userList
    for user in userList:
        if user.id == _id:
            return user
    return "invalid"    

def DeleteUserObject(username, password):
    ##username = input("Enter username: ")
    #password = input("Enter password: ")
    user = GetUserByUsername(username)
    if user == "invalid":
        print(f"user with username: {username} does not exist")
        return False
    if user.password == password:
        print(f"user with username: {username} deleted")
        os.remove(userDatabasePath+user.id)
        DeleteUser(user.id)
        return True
    print("Error: wrong password")
    return False

def DeleteUser(_id):
    userDatabaseFile = open(userDatabaseFilePath, "r")
    lines = userDatabaseFile.readlines()
    userDatabaseFile.close()
    tempLines = ""
    for line in lines:
        if _id not in line:
            tempLines += line + "\n"
    userDatabaseFile = open(userDatabaseFilePath, "w")
    userDatabaseFile.writelines(tempLines)
    userDatabaseFile.close()

def CreateNewNode(_username, _title, _text):
    user = GetUserByUsername(_username)
    node = modules.Node()
    node.title = _title
    node.text = _text
    user.nodeList.append(node)
    SaveUserObject(user)

def CheckCredentials(_username, _password):
    user = GetUserByUsername(_username)
    if user == "invalid":return False
    if user.password == _password:
        return True
    return False

def GetCookieData(_cookieValue):
    if _cookieValue == None:return"",""
    result = re.search(cookiePattern, _cookieValue)
    username = result.group(1)
    password = result.group(2)
    return username, password

def PrintDatabase():
    for user in userList:
        print(f"username >> {user.username}\npassword >> {user.password}\nid >> {user.id}\n\n")

def CreateRandomId():
    return hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()

def CreateMD5Hash(_input):
    return hashlib.md5(_input.encode()).hexdigest()

if __name__ == "__main__":
    try:
        command= sys.args[1]
    except:
        command = ""
    Run(command)