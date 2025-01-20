import requests

aws_url = (
    "https://s3.amazonaws.com:443/dev.challenge.com?"
    "list-type=2&prefix=&delimiter=%2F&encoding-type=url"
)
resp = requests.get(aws_url)
print(resp)
