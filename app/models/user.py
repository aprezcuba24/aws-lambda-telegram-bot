import os
import boto3
from datetime import datetime


region = os.environ.get("REGION")
dynamodb = boto3.resource("dynamodb", region_name=region)
USER_TABLE = os.environ.get("USER_TABLE")


def get_user_model(data):
    return {
        **data,
        **{
            "complete_name": f"{data.get('first_name', '')} {data.get('last_name', '')}"
        },
    }


def get_or_create_user(user_id, data):
    table = dynamodb.Table(USER_TABLE)
    user_id = str(user_id)
    Key = {"user_id": user_id}
    item = table.get_item(Key=Key)
    if "Item" in item:
        return get_user_model(item["Item"])
    now = datetime.now().isoformat()
    table.put_item(
        Item={
            **data,
            **{"user_id": user_id, "created_at": now, "updated_at": now},
        }
    )
    return get_user_model(table.get_item(Key=Key)["Item"])
