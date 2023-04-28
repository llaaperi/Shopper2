# Shopper2

## Install

### Google

```
https://console.developers.google.com/apis/credentials
```

1. Create project
2. Create OAuth consent screen
3. Create credentials, OAuth client ID
    - JavaScript origins: https://127.0.0.1:5000
    - Authorized redirect URIs: https://127.0.0.1:5000/login/callback


### App

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

export GOOGLE_CLIENT_ID=<client_id>
export GOOGLE_CLIENT_SECRET=<client_secret>
python app.py
