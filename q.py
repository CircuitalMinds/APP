from requests import get
url = "https://circuitalminds.github.io"
data = get(url).headers
print(data)