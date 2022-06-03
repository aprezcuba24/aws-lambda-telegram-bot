import boto3
import os
import time
from datetime import datetime, timedelta


def main(event, context):
    print(event)
    data = {item["code"]: item["value"] for item in event}
    print("send this data => ", data)


def calculate_data(event, context):
    region = os.environ.get("REGION")
    log_group = os.environ.get("MAIN_LOG_GROUP")
    logs_client = boto3.client("logs", region_name=region)
    start_query_response = logs_client.start_query(
        logGroupName=log_group,
        queryString=event["query"],
        startTime=int((datetime.today() - timedelta(hours=24)).timestamp()),
        endTime=int(datetime.now().timestamp()),
        limit=1,
    )
    query_id = start_query_response["queryId"]
    response = None
    while response == None or response["status"] == "Running":
        time.sleep(1)
        response = logs_client.get_query_results(queryId=query_id)
    return {
        "code": event["code"],
        "value": response["results"][0][0]["value"] if len(response["results"]) else 0,
    }
