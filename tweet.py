import json
import os
from datetime import datetime
import tweepy

# Twitter kimlik doğrulama
auth = tweepy.OAuth1UserHandler(
    os.getenv("TWITTER_API_KEY"),
    os.getenv("TWITTER_API_SECRET"),
    os.getenv("TWITTER_ACCESS_TOKEN"),
    os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
)
api = tweepy.API(auth)

# Tarih
today = datetime.today().strftime('%Y-%m-%d')

# Tatil ve ülke verilerini yükle
with open('holiday.json', 'r', encoding='utf-8-sig') as f:
    holidays = json.load(f)

with open('countries.json', 'r', encoding='utf-8-sig') as f:
    country_list = json.load(f)

# CountryCode → CountryName haritası oluştur
country_map = {c["code"].upper(): c["name"] for c in country_list}

# Tatilleri kontrol et
for country_code, holiday_list in holidays.items():
    for holiday in holiday_list:
        if holiday["date"].startswith(today):
            country_name = country_map.get(country_code.upper(), country_code)
            name = holiday["name"]
            url = f"https://holidayscalendar.com.tr/"

            tweet = (
                f"📅 {today} – Public Holiday in {country_name}\n"
                f"🎉 {name}\n\n"
                f"Details: {url}\n"
                f"#Holiday #{country_name.replace(' ', '')} #PublicHoliday"
            )

            try:
                api.update_status(tweet)
                print(f"✅ {tweet}")
            except Exception as e:
                print(f"❌ Failed for {country_name}: {e}")
