import requests
import qrcode

response = requests.post('http://localhost:1684/generate-token', json={
        'domain': 'http://localhost:1684', 
        'url': 'https://google.com/'
    }
)
data = response.json()

print(f"Generated Token: {data['token']}")
print(f"Generated URL: {data['url']}")

qr = qrcode.make(data['url'])
qr.save("one_time_qr.png")
print("QR code saved as one_time_qr.png")

use_response = requests.get(f"http://localhost:1684/use-token/{data['token']}")
print(f"Redirected to: {use_response.url}")