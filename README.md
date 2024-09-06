# One-Time QR Code Flask App

This is a simple Flask-based app that generates one-time-use QR codes with tokens. After scanning, if token is invalidated, the user is redirected to a specified URL.

## Public version | Example to use in directory tests [View](./tests/example.py) !!!
```url
https://shorten.sm1ky.com/
```

## Features
- Generates one-time-use tokens
- Redirects users after scanning the QR code
- Invalidates tokens after first use
- Docker and Poetry integration for easy setup

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sm1ky/one-time-qr.git
cd one-time-qr
```

### 2. Run the application using Docker Compose
```bash
docker compose up --build
```
