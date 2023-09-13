import requests

print(requests.__version__)

r = requests.get("https://raw.githubusercontent.com/Wanlin-Zheng/CMPUT404F2023/main/lab1.py")
print(r.text)

