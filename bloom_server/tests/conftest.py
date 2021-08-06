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

    credit_record = models.CreditRecords(
        name="Jane Doe",
        uuid="1337-1337-1337",
        ssn="123456789",
        x0001=123456789,
    )

    db.session.add(credit_record)
    db.session.commit()

    yield db

    db.session.remove()

    db.drop_all()

