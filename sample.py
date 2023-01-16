import os
import json
import csv
import boto3

from functions.check_origin import check_origin

client = boto3.client("s3")

BUCKET = os.environ["BUCKETNAME"]


def lambda_handler(event, context):
    print(event)
    if event.get('headers', {}).get('origin') and not check_origin(event["headers"]["origin"]):
        return {
            "statusCode": 403,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Requested-With,X-Requested-By,X-Api-Key",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Origin": event["headers"]["origin"],
            },
            "body": json.dumps({"message": "origin error"}),
        }

    response = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": BUCKET, "Key": "sample_image"},
        ExpiresIn=300,
        HttpMethod="GET",
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Requested-With,X-Requested-By,X-Api-Key",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"presigned_url": response}),
    }
