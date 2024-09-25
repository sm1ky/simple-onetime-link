import requests
#import qrcode

response = requests.post('https://shorten.sm1ky.com/generate-token', json={
        'domain': 'https://shorten.sm1ky.com', 
        'url': 'https://test.com'
    }
)
data = response.json()

print(f"Generated Token: {data['token']}")
print(f"Generated URL: {data['url']}")

use_response = requests.get(f"https://shorten.sm1ky.com/use-token/{data['token']}")
print(f"Redirected to: {use_response.url}")
