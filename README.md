# YouTube VOD Auto Uploader

This project automates uploading Twitch VODs to YouTube using the YouTube Data API. It is designed to run headlessly on a Debian server (SERVERBOX) and uses OAuth2 authentication for YouTube access.

---

## Requirements

- Python 3.10+
- `virtualenv` for environment isolation
- Google API credentials
- A local machine (with a browser) for one-time token generation

---

## Setup Instructions

### 1. Clone and prepare environment

```bash
git clone [your-repo]
cd twitchvod
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 2. Get Google OAuth credentials

1. Go to https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Enable the **YouTube Data API v3**
4. Go to **APIs & Services > Credentials**
5. Create **OAuth 2.0 Client ID**
   - Application type: **Desktop App**
6. Download the `client_secret.json` and place it in the project root.

---

### 3. Generate token on a system with a browser

```bash
python get_youtube_token_local.py
```

- This opens a browser window.
- Login and click **Allow**.
- A file `token.json` will be created.

**Check it has a refresh token:**

```bash
cat token.json | jq '.refresh_token'
```

If it's `null`, revoke app permissions [here](https://myaccount.google.com/permissions), then try again.

---

### 4. Deploy to SERVERBOX

```bash
scp client_secret.json token.json spraggs@SERVERBOX:~/twitchvod/
```

---

### 5. Run the uploader on SERVERBOX

```bash
cd ~/twitchvod
source venv/bin/activate
python get_latest_vod_auto.py
```

---

## Files

- `get_youtube_token_local.py`: Auth flow to generate `token.json`
- `get_latest_vod_auto.py`: Main upload script
- `client_secret.json`: Google OAuth credentials (do not share)
- `token.json`: Auth token with refresh capability (regenerate if expired)

---

## Notes

- Do not regenerate `token.json` without also updating `client_secret.json`
- Refresh token only works with the original client ID that created it
- Tokens are stored locally in `token.json` and can be reused until revoked or expired
