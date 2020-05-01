from json import loads, dumps
import requests
import tempfile
import os
import shutil
from datetime import date
from helpers.s3 import push_file_to_s3

S3_BUCKET = str(os.getenv('BILL_BUCKET'))
today = date.today()

bill_stem = 'bill_text'
url_base = 'https://www.govinfo.gov/bulkdata/BILLS/'

def handler(event, context):
    print('Start of download process')
    for item in event['Records']:
        try:
            message = loads(item['body'])
            cong = message.get('congress')
            sess = message.get('session')

            target = url_base + '%d/%d/s/BILLS-%d-%d-s.zip' % (cong, sess, cong, sess)
            r = requests.get(target, stream=True)
            chunk_size = 8192

            with tempfile.TemporaryDirectory() as tmpdir:
                os.chdir(tmpdir)

                filename = '%s-%s.zip' % (cong, sess)
                save_path = os.path.join(os.getcwd(), filename)
                with open(save_path, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        fd.write(chunk)
                    print('Copied download file locally from %s' % target)

                key = 'zip_downloads/' + str(today.strftime("%Y-%m-%d"))
                push_file_to_s3(
                    os.getcwd(),
                    filename,
                    S3_BUCKET,
                    key
                )
                print('Wrote zip file to s3://%s/%s/%s' % (S3_BUCKET, key, filename))

        except Exception as e:
            print('Unable to complete download: %s' % dumps(item))
            print(repr(e))
