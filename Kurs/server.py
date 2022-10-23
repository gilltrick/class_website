from flask import Flask, request, render_template, make_response
from website import database

server = Flask(__name__)
username = ""


@server.route("/api/in", methods=["post"])
def api_in():
    global username
    username = request.form["username"]
    print(f"username: {username}")
    return "ok"

@server.route("/api/out", methods=["get"])
def api_out():
    global username
    data = {"username":username}
    return data

@server.route("/")
def index():
    return render_template("index.html")

@server.route("/register")
def register():
    return render_template("register.html")

@server.route("/login")
def login():
    return render_template("login.html")

@server.route("/registerUser", methods=["post"])
def registerUser():
    username = database.CreateMD5Hash(request.form["username"])
    password = database.CreateMD5Hash(request.form["password"])
    #print(f"username: {username}\npassword: {password}")
    user = database.CreateUser(username, password)
    print(f"userid >> {user.id}")
    return "ok"

@server.route("/loginUser", methods=["post"])
def loginUser():
    username = database.CreateMD5Hash(request.form["username"])
    password = database.CreateMD5Hash(request.form["password"])
    #print(f"username: {username}\npassword: {password}")
    if database.CheckCredentials(username, password):
        user = database.GetUserByUsername(username)
        cookieValue = f"username:{username};password:{password}"
        response = make_response(render_template("home.html", user=user))  
        response.set_cookie("data", cookieValue)
        return response
    return "error"  
    
@server.route("/home")
def home():
    cookieValue = request.cookies.get("data")
    username,password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        user = database.GetUserByUsername(username)
        return render_template("home.html", user=user)
    return render_template("register.html")

@server.route("/logout")
def logout():
    cookieValue = request.cookies.get("data")
    username,password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        response = make_response(render_template("logout.html"))  
        response.set_cookie("data", expires=0)
        return response
    return "error"

@server.route("/delete")
def delete():
    return render_template("delete.html")

@server.route("/deleteUser", methods=["post"])
def deleteUser():
    username = database.CreateMD5Hash(request.form["username"])
    password = database.CreateMD5Hash(request.form["password"])
    if database.DeleteUserObject(username, password):
        return "ok"
    return "error"

@server.route("/newNode", methods=["post"])
def newNode():
    cookieValue = request.cookies.get("data")
    username,password = database.GetCookieData(cookieValue)
    if database.CheckCredentials(username, password):
        title = request.form["title"]
        text = request.form["text"]
        user = database.GetUserByUsername(username)
        database.CreateNewNode(username, title, text)
        return render_template("home.html", user=user)
    return "error"

if __name__ == "__main__":
    database.InitDB()
    server.run(debug=True, host="0.0.0.0", port=1234)