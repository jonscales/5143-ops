import requests
from rich import print

r = requests.get("http://sendmessage.live:8001/grayscale?num=100")

print(r.json())
