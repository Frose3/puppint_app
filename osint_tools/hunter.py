import os

from django.db.models.fields import return_None
from dotenv import load_dotenv
import requests


def hunter(user_query):
    try:
        load_dotenv(dotenv_path="api.env")
        hunter_api_key = os.getenv("HUNTER_API_KEY")

        response = requests.get(f"https://api.hunter.io/v2/domain-search?domain={user_query}&api_key={hunter_api_key}")

        result = response.json()['data']

        data = {
            "domain": result["domain"],
            "webmail": result["webmail"],
            "organization": result["organization"],
            "description": result["description"],
            "industry": result["industry"],
            "twitter": result["twitter"],
            "facebook": result["facebook"],
            "linkedin": result["linkedin"],
            "instagram": result["instagram"],
            "youtube": result["youtube"],
            "country": result["country"],
            "city": result["city"],
        }

        emails = []
        for email in result["emails"]:
            email_data = {
                "email": email['value'],
                "type": email['type'],
                "firstname": email['first_name'],
                "lastname": email['last_name'],
                "position": email['position'],
                "department": email['department'],
                "linkedin": email['linkedin'],
                "twitter": email['twitter'],
                "phone_number": email['phone_number'],
                "valid": email['verification']['status']
            }
            emails.append(email_data)

        return {"data": data, "emails": emails }

    except Exception as e:
        print(e)
        return e