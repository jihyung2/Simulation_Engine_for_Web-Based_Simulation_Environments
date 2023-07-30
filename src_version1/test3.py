import requests

import requests

url = "http://localhost:8700/api"
response = requests.post(url, data="asda")

print(response.json())