from bloom_database.models import models
import uuid


def test_credit_record_model():

    credit_record_uuid = str(uuid.uuid4())

    credit_record = models.CreditRecords(
        name="Jane Doe",
        uuid=credit_record_uuid,
        ssn="123456789",
        x0001=123456789,
    )

    assert credit_record.name == "Jane Doe"
    assert credit_record.uuid == credit_record_uuid
    assert credit_record.ssn == "123456789"
    assert credit_record.x0001 == 123456789
    assert credit_record.x0002 == None