
import requests

response = requests.post('https://shorten.sm1ky.com/generate-token', json={
        'domain': 'https://shorten.sm1ky.com', 
        'url': 'https://test.com',
        'length': 6
    }
)
data = response.json()

print(f"Generated Token: {data['token']}")
print(f"Generated URL: {data['url']}")

use_response = requests.get(data['url'])
print(f"Redirected to: {use_response.url}")
