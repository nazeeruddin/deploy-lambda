
import json
import requests
import certifi
import os

def lambda_handler(event, context):

    country = event.get("country", "India")

    url = (
        "https://api.restcountries.com/"
        f"countries/v5/names.common/{country}"
    )

    headers = {
        "Authorization": (
            f"Bearer {os.environ['REST_COUNTRIES_API_KEY']}"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            verify=certifi.where()
        )

        response.raise_for_status()
        data = response.json()

        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }

    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 502,
            "body": json.dumps({
                "error": str(e)
            })
        }
