import json
import urllib.parse

from app.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    DISCORD_TOKEN_ENDPOINT,
    REDIRECT_URI,
)
from app.client import Client


def get_api_access_token_from_authorization_code(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    api_client = Client(
        method="post",
        url=DISCORD_TOKEN_ENDPOINT,
        data=urllib.parse.urlencode(data, doseq=True),
        headers=headers,
    )

    try:
        status_code, data = api_client.make_request()
    except Exception as e:
        print(e)
    finally:
        return data.get("access_token", None), data.get("webhook", {}).get("url", None)


def post_question_to_channel_using_incoming_webhook(question, webhook_url):
    headers = {
        "Content-Type": "application/json",
    }
    api_client = Client(
        "post", url=webhook_url, data=json.dumps(question), headers=headers
    )
    try:
        status_code, data = api_client.make_request()
    except Exception as e:
        print(e)
    else:
        return status_code
