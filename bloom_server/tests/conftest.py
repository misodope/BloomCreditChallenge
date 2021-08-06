import os
import tempfile

import pytest

from bloom_server.app import app
from bloom_database.models import db, models


@pytest.fixture()
def client():
    app.config['TESTING'] = True
    app.config['DEBUG'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture()
def init_database():

    db.create_all()

    credit_record_1 = models.CreditRecords(
        name="Jane Doe",
        uuid="1337-1337-1337",
        ssn="123456789",
        x0001=100,
    )

    db.session.add(credit_record_1)
    db.session.commit()

    credit_record_2 = models.CreditRecords(
        name="Jane Doe",
        uuid="123-123-123",
        ssn="987654321",
        x0001=50,
    )

    db.session.add(credit_record_2)
    db.session.commit()

    yield db

    db.session.remove()

    db.drop_all()

