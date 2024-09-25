
# Пример использования

## Синхронный запрос с помощью requests

```python
import requests

response = requests.post('https://shorten.sm1ky.com/generate-token', json={
        'domain': 'https://shorten.sm1ky.com', 
        'url': 'https://test.com',
        'length': 6
    }
)
data = response.json()

print(f"Сгенерированный токен: {data['token']}")
print(f"Сгенерированный URL: {data['url']}")

# Проверяем перенаправление
use_response = requests.get(data['url'])
print(f"Перенаправлено на: {use_response.url}")
```

## Асинхронный запрос с помощью aiohttp

```python
import aiohttp
import asyncio

async def shorten_url():
    async with aiohttp.ClientSession() as session:
        async with session.post('https://shorten.sm1ky.com/generate-token', json={
            'domain': 'https://shorten.sm1ky.com',
            'url': 'https://test.com',
            'length': 6
        }) as response:
            data = await response.json()
            print(f"Сгенерированный токен: {data['token']}")
            print(f"Сгенерированный URL: {data['url']}")
            
            # Проверяем перенаправление
            async with session.get(data['url']) as use_response:
                print(f"Перенаправлено на: {use_response.url}")

asyncio.run(shorten_url())
```

## Асинхронный запрос с помощью httpx

```python
import httpx
import asyncio

async def shorten_url():
    async with httpx.AsyncClient() as client:
        response = await client.post('https://shorten.sm1ky.com/generate-token', json={
            'domain': 'https://shorten.sm1ky.com',
            'url': 'https://test.com',
            'length': 6
        })
        data = response.json()
        print(f"Сгенерированный токен: {data['token']}")
        print(f"Сгенерированный URL: {data['url']}")
        
        # Проверяем перенаправление
        use_response = await client.get(data['url'])
        print(f"Перенаправлено на: {use_response.url}")

asyncio.run(shorten_url())
```


- [Назад](README.md)