"""Shared boto3 DynamoDB resource factory (AWS or DynamoDB Local)."""

import os

import boto3


def get_dynamodb_resource():
    """Return a boto3 DynamoDB resource, optionally pointing at DynamoDB Local."""
    region = os.environ.get("REGION", "us-east-1")
    endpoint = os.environ.get("DYNAMODB_ENDPOINT")
    kwargs = {"region_name": region}
    if endpoint:
        kwargs["endpoint_url"] = endpoint
    return boto3.resource("dynamodb", **kwargs)


def get_dynamodb_client():
    """Return a boto3 DynamoDB *client* (same endpoint/region as get_dynamodb_resource)."""
    region = os.environ.get("REGION", "us-east-1")
    endpoint = os.environ.get("DYNAMODB_ENDPOINT")
    kwargs = {"region_name": region}
    if endpoint:
        kwargs["endpoint_url"] = endpoint
    return boto3.client("dynamodb", **kwargs)


def is_local_dynamo_dev() -> bool:
    """True when using local DynamoDB or explicit LOCAL_DEV (skip AWS-only embedded metrics)."""
    if os.environ.get("DYNAMODB_ENDPOINT"):
        return True
    return os.environ.get("LOCAL_DEV", "").lower() in ("1", "true", "yes")
