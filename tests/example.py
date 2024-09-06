import requests
import qrcode

response = requests.post('https://shorten.sm1ky.com/generate-token', json={
        'domain': 'https://shorten.sm1ky.com', 
        'url': 'https://google.com/'
    }
)
data = response.json()

print(f"Generated Token: {data['token']}")
print(f"Generated URL: {data['url']}")

qr = qrcode.make(data['url'])
qr.save("one_time_qr.png")
print("QR code saved as one_time_qr.png")

use_response = requests.get(f"https://shorten.sm1ky.com/use-token/{data['token']}")
print(f"Redirected to: {use_response.url}")
