from bloom_database.models import models, db
from http import HTTPStatus

from . import create_app


app = create_app()

@app.route('/')
def index():
    return "Hi Bloom Credit."

@app.route('/credit_record/get/<consumer_id>', methods=['GET'])
def get_credit_record(consumer_id):

    credit_record = (
        db.session.query(*[c.label(c.name) for c in models.CreditRecords.__table__.columns])
        .filter(models.CreditRecords.uuid == consumer_id)
    ).one_or_none()

    if not credit_record:
        return { "message": f"Credit record with ID {consumer_id} not found." }, HTTPStatus.NOT_FOUND

    credit_record_dict = credit_record._asdict()

    return credit_record_dict, HTTPStatus.OK

@app.route('/credit_tag/statistics/get/<credit_tag>', methods=['GET'])
def get_consumer_statistics(credit_tag):

    statistics = (
        db.session.execute(
            f"""
                SELECT cast(avg({credit_tag}) as text) as mean, cast(stddev({credit_tag}) as text) as stddev, (
                    SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY {credit_tag}) FROM credit_records
                ) as median
                FROM credit_records
                WHERE {credit_tag} IS NOT NULL
            """
        )
    ).one_or_none()

    if not statistics:
        return { "message": f"Statistics not calculating correctly for: {credit_tag}" }, HTTPStatus.NOT_FOUND

    statistics_dict = statistics._asdict()

    return statistics_dict, HTTPStatus.OK

if __name__ == '__main__':
    app.run()