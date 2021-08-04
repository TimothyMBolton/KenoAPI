import requests

URL = 'https://api-info-nsw.keno.com.au/v2/info/history?jurisdiction=NSW'

response = requests.get(URL)
size = len(response.content)
size = size * 12 * 24
size /= 1000000
print(size)

