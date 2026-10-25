
import json
import requests
import certifi
import os
import logging
import time
from urllib.parse import quote

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    start_time = time.perf_counter()

    country = event.get("country", "India")
    request_id = (
        context.aws_request_id if context else "local-test"
    )

    logger.info(
        "Lambda started | RequestId=%s | Country=%s",
        request_id,
        country
    )

    url = (
        "https://api.restcountries.com/"
        f"countries/v5/names.common/{quote(str(country), safe='')}"
    )

    try:
        api_key = os.environ["REST_COUNTRIES_API_KEY"]

        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        logger.info("Calling REST Countries API")

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            verify=certifi.where()
        )

        logger.info(
            "API response received | StatusCode=%s",
            response.status_code
        )

        response.raise_for_status()
        data = response.json()

        logger.info(
            "API response parsed successfully | Country=%s",
            country
        )

        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }

    except requests.exceptions.Timeout:
        logger.warning(
            "API request timed out | Country=%s",
            country
        )

        return {
            "statusCode": 504,
            "body": json.dumps({
                "error": "External API timed out"
            })
        }

    except requests.exceptions.RequestException:
        logger.exception(
            "API request failed | Country=%s",
            country
        )

        return {
            "statusCode": 502,
            "body": json.dumps({
                "error": "External API request failed"
            })
        }

    except (KeyError, ValueError):
        logger.exception(
            "Configuration or response processing failed"
        )

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal processing error"
            })
        }

    finally:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.info(
            "Lambda execution completed | "
            "RequestId=%s | DurationMs=%.2f",
            request_id,
            duration_ms
        )