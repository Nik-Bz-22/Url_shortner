import os
import json
import string
import random
import time
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def get_short_urlr(event, base_url:str) -> str|None:
    try:
        body = json.loads(event.get("body", "{}"))
        original_url = body.get("url")
        if not original_url:
            get_short_urlr.status = {
                "statusCode": 400,
                "body": json.dumps({"error": "URL is required"}),
            }
            return None

    except Exception:
        get_short_urlr.status = {
            "statusCode": 400,
            "body": json.dumps({"error": "Incorrect JSON"})
        }
        return None

    short_id = generate_short_id()

    expires_at = int(time.time()) + 15 * 60

    table.put_item(Item={
        "short_id": short_id,
        "original_url": original_url,
        "expires_at": expires_at
    })

    short_url = base_url + short_id
    return short_url


def resolve_short_url(path_parameters) -> str|None:
    short_id = path_parameters["short_id"]
    response = table.get_item(Key={"short_id": short_id})
    if "Item" not in response:
        resolve_short_url.status = {
            "statusCode": 404,
            "body": json.dumps({"error": "URL not found"})
        }
        return None
    original_url = response["Item"]["original_url"]
    return original_url

def handler(event, context):
    http_method = event.get("httpMethod")
    path_parameters = event.get("pathParameters") or {}
    r_context = event.get("requestContext") or {}
    base_url = "https://" + r_context["domainName"] + "/" + r_context["stage"] + "/"

    if http_method == "POST" and event.get("resource") == "/shorten":
        short_url = get_short_urlr(event=event, base_url=base_url)

        if not short_url:
            return get_short_urlr.status
        return {
            "statusCode": 200,
            "body": json.dumps({"short_url": short_url})
        }

    elif http_method == "GET" and "short_id" in path_parameters:
        original_url = resolve_short_url(path_parameters=path_parameters)
        if not original_url:
            return resolve_short_url.status
        return {
            "statusCode": 301,
            "headers": {
                "Location": original_url
            },
            "body": ""
        }

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Method Not Allowed"})
        }
