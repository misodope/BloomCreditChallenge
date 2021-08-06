import codecs
import requests
import tempfile
import uuid

from bz2 import BZ2Decompressor

from bloom_database.models import models
from bloom_server.app import app_db as meta


class CreditRecordParser:
    def __init__(self):
        pass

    def run():

        rows = []

        with tempfile.TemporaryFile() as tfp:
            with requests.get("https://bloom-data-engineering-challenge.s3.amazonaws.com/test.dat.bz2", stream=True) as r:
                decompressor = BZ2Decompressor()

                for chunk in r.iter_content(chunk_size=1024 * 8):
                    chunk = decompressor.decompress(chunk)
                    tfp.write(chunk)

            tfp.seek(0)

            decoded_fp = codecs.getreader("utf-8")(tfp)

            lines = decoded_fp.readlines()

            for line in lines[1:]:
                consumer_uuid = str(uuid.uuid4())
                name = line[:72].strip()
                ssn = line[73:81].strip()

                credit_record = {
                    "uuid": consumer_uuid,
                    "name": name,
                    "ssn": ssn,
                }

                credit_tags_start = line[81:]
                current_tag = 1

                for index in range(0, len(credit_tags_start), 9):

                    credit_tag = credit_tags_start[index : index + 9].strip()

                    if credit_tag:
                        try:
                            credit_tag_exists = int(credit_tag) < 0

                            if not credit_tag_exists:
                                credit_record["x" + f"{current_tag}".zfill(4)] = credit_tag
                            else:
                                credit_record["x" + f"{current_tag}".zfill(4)] = None

                        except:
                            credit_record["x" + f"{current_tag}".zfill(4)] = None

                    current_tag += 1

                rows.append(credit_record)

                if len(rows) > 5000:
                    meta.session.execute(
                        models.CreditRecords.__table__.insert()
                        .values(rows)
                    )
                    meta.session.commit()
                    rows=[]

            if rows:
                meta.session.execute(
                    models.CreditRecords.__table__.insert()
                    .values(rows)
                )

            meta.session.commit()
