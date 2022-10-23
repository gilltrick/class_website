import requests

url = "http://192.168.2.100:1234/api/"

requests.post(url+"in", data = {"username":"patrick"})
print(requests.get(url+"out").json()["username"])