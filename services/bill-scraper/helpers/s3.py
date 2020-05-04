from json import dumps
from boto3 import client, resource
import os

S3_CLIENT = client('s3')
S3_RESOURCE = resource('s3')


def get_matching_s3_objects(bucket, prefix='', suffix=''):
	"""
	Generate objects in an S3 bucket.
	Source: https://alexwlchan.net/2019/07/listing-s3-keys/

	:param bucket: Name of the S3 bucket.
	:param prefix: Only fetch objects whose key starts with
		this prefix (optional).
	:param suffix: Only fetch objects whose keys end with
		this suffix (optional).
	"""
	paginator = S3_CLIENT.get_paginator('list_objects_v2')

	kwargs = {'Bucket': bucket}

	# We can pass the prefix directly to the S3 API.  If the user has passed
	# a tuple or list of prefixes, we go through them one by one.
	if isinstance(prefix, str):
		prefixes = (prefix,)
	else:
		prefixes = prefix

	for key_prefix in prefixes:
		kwargs['Prefix'] = key_prefix

		for page in paginator.paginate(**kwargs):
			try:
				contents = page['Contents']
			except KeyError:
				break

			for obj in contents:
				key = obj['Key']
				if key.endswith(suffix):
					yield obj


def get_matching_s3_keys(bucket, prefix='', suffix=''):
	"""
	Generate the keys in an S3 bucket.

	:param bucket: Name of the S3 bucket.
	:param prefix: Only fetch keys that start with this prefix (optional).
	:param suffix: Only fetch keys that end with this suffix (optional).
	"""
	for obj in get_matching_s3_objects(bucket, prefix, suffix):
		yield obj['Key']


def has_matching_s3_key(bucket, prefix='', suffix=''):
	obj_gen = get_matching_s3_keys(bucket, prefix, suffix)
	try:
		next(obj_gen)
	except StopIteration:
		return False
	return True


def read_event_files(event):
	data = event['Records']
	files = []
	for item in data:
		file = {
			'bucket': item['s3']['bucket']['name'],
			'key': item['s3']['object']['key']
		}
		files.append(file)
	print('Finished reading event files')
	return files


def read_s3_contents(bucket, key):
	obj = S3_RESOURCE.Object(Bucket=bucket, Key=key)
	file_data = obj.get()['Body']
	return file_data


def push_file_to_s3(local_file_path, file_name, bucket_name, s3_path=''):
	"""
	Push file into S3 bucket
	:param bucket_name: str
	:param file_name: str
	:param local_file_path: str
	:param s3_path: str

	:return: Nothing
	"""
	if len(s3_path) > 0 and s3_path[-1:] != '/':
		s3_path += '/'
	# print('Pushing file %s to bucket %s%s' % (file_name, bucket_name, s3_path))
	with open(os.path.join(local_file_path, file_name), 'rb') as data:
		s3_output = S3_RESOURCE.Bucket(bucket_name).put_object(
			Key=s3_path + file_name,
			Body=data,
		)
		# print(s3_output)


def push_object_to_s3(obj, file_name, bucket_name, s3_path=''):
	"""
	:param obj: object
	:param file_name: str (with extension)
	:param bucket_name: str
	:param s3_path: str
	:return: Nothing
	"""
	if len(s3_path) > 0 and s3_path[-1:] != '/':
		s3_path += '/'
	# print('Pushing data to file %s in bucket %s%s' % (file_name, bucket_name, s3_path))
	s3_output = S3_CLIENT.put_object(
		Body=dumps(obj),
		Bucket=bucket_name,
		Key=s3_path + file_name,
	)
	# print(s3_output)


def push_data_to_s3(data, file_name, bucket_name, s3_path=''):
	"""
	:param data: bytes type
	:param file_name: str (with extension)
	:param bucket_name: str
	:param s3_path: str
	:return: Nothing
	"""
	if len(s3_path) > 0 and s3_path[-1:] != '/':
		s3_path += '/'
	# print('Pushing data to file %s in bucket %s%s' % (file_name, bucket_name, s3_path))
	s3_output = S3_CLIENT.put_object(
		Body=data,
		Bucket=bucket_name,
		Key=s3_path + file_name,
	)
	# print(s3_output)
