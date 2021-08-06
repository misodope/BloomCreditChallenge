from http import HTTPStatus
from bloom_database.models import models, db
from flask import json


def test_api_default_get_endpoint(client):

    response = client.get('/')

    data = response.data.decode('utf-8')

    assert response.status_code == HTTPStatus.OK
    assert data == "Hi Bloom Credit."


def test_api_credit_record_get_invalid_consumer_id(client, init_database):

    response = client.get('/credit_record/get/1234')

    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["message"] == "Credit record with ID 1234 not found."


def test_api_credit_record_get(client, init_database):

    response = client.get('/credit_record/get/1337-1337-1337')

    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == HTTPStatus.OK
    assert data["name"] == "Jane Doe"
    assert data["ssn"] == "123456789"

