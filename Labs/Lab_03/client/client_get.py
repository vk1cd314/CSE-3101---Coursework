import requests

url = "http://localhost:8080/hello.txt"
response = requests.get(url)

if response.status_code == 200:
    with open("hello.txt", "wb") as f:
        f.write(response.content)
        print("Successfully written to local storage")
else:
    print("Failed to download file:", response.status_code)