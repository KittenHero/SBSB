import json
import pytest

from api.app import purchase


def test_purchase(mocker):
    with open('events/purchase.json') as f:
        event = json.load(f)

    ret = purchase(event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    print(data)
