
# Example Usage of URL Shortening with Synchronous and Asynchronous Requests

This example demonstrates how to use synchronous requests with `requests` and asynchronous requests with `aiohttp` and `httpx` to shorten URLs using the `shorten.sm1ky.com` service.

## Synchronous Example with `requests`

```python
import requests

# Sync. Requests
response = requests.post('https://shorten.sm1ky.com/generate-token', json={
        'domain': 'https://shorten.sm1ky.com', 
        'url': 'https://test.com',
        'length': 6
    }
)
data = response.json()

print(f"Generated Token: {data['token']}")
print(f"Generated URL: {data['url']}")

# Follow the shortened link
use_response = requests.get(data['url'])
print(f"Redirected to: {use_response.url}")
```

## Asynchronous Example with `aiohttp`

```python
import aiohttp
import asyncio

async def generate_token():
    async with aiohttp.ClientSession() as session:
        # Sending POST request to generate token
        async with session.post('https://shorten.sm1ky.com/generate-token', json={
            'domain': 'https://shorten.sm1ky.com',
            'url': 'https://test.com',
            'length': 6
        }) as response:
            data = await response.json()
            print(f"Generated Token: {data['token']}")
            print(f"Generated URL: {data['url']}")

        # Redirecting to the shortened URL
        async with session.get(data['url']) as use_response:
            print(f"Redirected to: {use_response.url}")

# Running the async function
asyncio.run(generate_token())
```

## Asynchronous Example with `httpx`

```python
import httpx
import asyncio

async def generate_token():
    async with httpx.AsyncClient() as client:
        # Sending POST request to generate token
        response = await client.post('https://shorten.sm1ky.com/generate-token', json={
            'domain': 'https://shorten.sm1ky.com',
            'url': 'https://test.com',
            'length': 6
        })
        data = response.json()
        print(f"Generated Token: {data['token']}")
        print(f"Generated URL: {data['url']}")

        # Redirecting to the shortened URL
        use_response = await client.get(data['url'])
        print(f"Redirected to: {use_response.url}")

# Running the async function
asyncio.run(generate_token())
```

### Conclusion

The examples above show how to perform both synchronous and asynchronous HTTP requests to shorten URLs using different Python libraries. Depending on the complexity of your application and whether it benefits from asynchronous I/O, you can choose between `requests`, `aiohttp`, and `httpx`.

- [Back](README.md)