import requests

Headers = {"Authorization" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyNjEyMjg5LCJpYXQiOjE2NTI2MTE5ODksImp0aSI6ImQwMzZjMmMxNTY2NDRmODViZWU1MTEwYzIyZTNhMzE3IiwidXNlcl9pZCI6Ik5vbmUifQ.7EabK0mce7ijYFA2L-E15-aGhEiasb3LeG52Wuk8Ny4" }
dupa = requests.get("http://0.0.0.0:8002/", headers=Headers ).json()
print(dupa)