from http import HTTPStatus
from flask import json
from decimal import Decimal


def test_api_default_get_endpoint(client):

    response = client.get('/')

    data = response.data.decode('utf-8')

    assert response.status_code == HTTPStatus.OK
    assert data == "Hi Bloom Credit."


def test_api_credit_record_get(client, init_database):

    response = client.get('/credit_record/get/1337-1337-1337')

    data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == HTTPStatus.OK
    assert data["name"] == "Jane Doe"
    assert data["ssn"] == "123456789"


def test_api_credit_record_get_invalid_consumer_id(client, init_database):

    response = client.get('/credit_record/get/1234')

    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["message"] == "Credit record with ID 1234 not found."


def test_api_credit_tag_get(client, init_database):

    response = client.get('/credit_tag/statistics/get/x0001')

    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == HTTPStatus.OK
    assert Decimal(data["mean"]) == Decimal('75.00')
    assert Decimal(data["median"]) == Decimal('75.00')
    assert Decimal(data["stddev"]) == Decimal('35.3553390593273762')


def test_api_credit_tag_get(client, init_database):

    response = client.get('/credit_tag/statistics/get/x1337')

    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert data["message"] == "Statistics not calculating correctly for: x1337"

