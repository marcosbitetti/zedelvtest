import pytest
import asyncio
import pytest_asyncio
import os
from dotenv import load_dotenv

import common.db as db
import resources.partners as partners

TEST_DATA_INSERT = {
    "tradingName": "TESTE Adega Osasco ",
    "ownerName": "Ze da Ambev",
    "document": "02.453.716/000170",
    "coverageArea": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [ -43.36556, -22.99669 ],
                    [ -43.36539, -23.01928 ],
                    [ -43.26583, -23.01802 ],
                    [ -43.36556, -22.99669 ]
                ]
            ]
        ]
    },
    "address": {
        "type": "Point",
        "coordinates": [ -43.297337, -23.013538 ]
    }
}

def test_app_configuration():
    load_dotenv()
    assert os.getenv('app_name') != None
    db.initialize()


def test_migrate():
    db.migrate()


def test_partners_get():
    dt = partners.get(1)
    assert type(dt) is dict
    assert dt['tradingName'] == 'Adega Osasco'

def test_partners_search():
    dt = partners.search(lat=-43.297337, lon=-23.013538, radius=10)
    assert type(dt) is list
    assert len(dt) == 5


def test_partners_create_prevent_key_duplication():
    dt = partners.create(TEST_DATA_INSERT)
    assert type(dt) == dict
    assert dt['status'] == 'error'

def test_partners_create():
    insert = TEST_DATA_INSERT
    insert['document'] = '02.453.716/888888'
    dt = partners.create(insert)
    assert type(dt) == dict
    assert dt['status'] == 'ok'

