#!/usr/bin/env python3
"""Create DynamoDB tables on the configured endpoint (DynamoDB Local or AWS).

Schemas match resources/dynamodb.yml. Run from project root, e.g.:
  python scripts/create_tables.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# Project root on sys.path for `app` imports
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

try:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=_ROOT / ".envs" / ".local" / ".app")
except ImportError:
    pass

import os

from botocore.exceptions import ClientError

from app.utils.dynamodb import get_dynamodb_resource


def _ensure_table(name: str, hash_key: str, hash_type: str) -> None:
    client = get_dynamodb_resource().meta.client
    try:
        client.describe_table(TableName=name)
        print(f"Table {name!r} already exists.")
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code != "ResourceNotFoundException":
            raise
        client.create_table(
            TableName=name,
            AttributeDefinitions=[
                {"AttributeName": hash_key, "AttributeType": hash_type},
            ],
            KeySchema=[{"AttributeName": hash_key, "KeyType": "HASH"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        print(f"Created table {name!r}.")


def main() -> None:
    user_table = os.environ.get("USER_TABLE")
    persistence_table = os.environ.get("PERSISTENCE_TABLE")
    if not user_table or not persistence_table:
        print(
            "USER_TABLE and PERSISTENCE_TABLE must be set (e.g. via .envs/.local/.app).",
            file=sys.stderr,
        )
        sys.exit(1)
    _ensure_table(user_table, "user_id", "S")
    _ensure_table(persistence_table, "persistence_id", "S")


if __name__ == "__main__":
    main()
