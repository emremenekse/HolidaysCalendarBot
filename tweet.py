import os
import json
import requests
from requests_oauthlib import OAuth1
from datetime import datetime

# Twitter OAuth 1.0 kimlik doğrulama
auth = OAuth1(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)

# Tarih
today = datetime.today().strftime('%Y-%m-%d')

# JSON dosyaları
with open("holiday.json", encoding="utf-8-sig") as f:
    holidays = json.load(f)

with open("countries.json", encoding="utf-8-sig") as f:
    country_list = json.load(f)

# Ülke kodu -> isim
country_map = {c["code"].upper(): c["name"] for c in country_list}

# Her tatil için ayrı tweet
for country_code, holiday_list in holidays.items():
    for holiday in holiday_list:
        if holiday["date"].startswith(today):
            country_name = country_map.get(country_code.upper(), country_code)
            name = holiday["name"]
            url = f"https://holidayscalendar.com.tr/"

            tweet_text = (
                f"📅 {today} – Public Holiday in {country_name}\n"
                f"🎉 {name}\n\n"
                f"Details: {url}\n"
                f"#Holiday #{country_name.replace(' ', '')} #PublicHoliday"
            )

            payload = {"text": tweet_text}

            response = requests.post(
                "https://api.twitter.com/2/tweets",
                auth=auth,
                json=payload
            )

            if response.status_code == 201:
                print(f"✅ Tweet sent: {tweet_text}")
            else:
                print(f"❌ Failed: {response.status_code} – {response.text}")
