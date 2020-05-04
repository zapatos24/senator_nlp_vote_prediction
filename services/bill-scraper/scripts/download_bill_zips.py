import requests
import os

downloads = '../bill_data/'
url_base = 'https://www.govinfo.gov/bulkdata/BILLS/'


if not os.path.exists(downloads):
	os.makedirs(downloads)


def download_url(url, save_path, chunk_size=128):
	r = requests.get(url, stream=True)
	with open(save_path, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=chunk_size):
			fd.write(chunk)


for cong in range(113, 116 + 1):
	for sess in range(1, 2 + 1):
		zip = url_base + '%d/%d/s/BILLS-%d-%d-s.zip' % (cong, sess, cong, sess)
		download_url(zip, downloads + '%s-%s.zip' % (cong, sess))


