import requests

bucket_url = "https://s3.amazonaws.com:443/dev.challenge.com?list-type=2&prefix=&delimiter=%2F&encoding-type=url"
response = requests.get(bucket_url)
print(response)