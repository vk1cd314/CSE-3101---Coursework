import requests

url = "http://localhost:8080/"
file_path = "nani.txt"

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print(response.text)