from json import dumps
from boto3 import client

SQS_CLIENT = client('sqs')


def enqueue_message(message, queue_name):
	"""
	Adds message to the queue
	:param message: object
	:param queue_name: str (url)
	:return: Nothing
	"""
	message_str = dumps(message)
	queue_url = _get_queue_url(queue_name)
	SQS_CLIENT.send_message(QueueUrl=queue_url, MessageBody=message_str)
	# print('Enqueued to %s: %s' % (queue_url, message_str))


def long_poll_queue(queue_name, num_messages):
	response = SQS_CLIENT.receive_message(
		QueueUrl=_get_queue_url(queue_name),
		AttributeNames=[
			'SentTimestamp'
		],
		MaxNumberOfMessages=num_messages,
		MessageAttributeNames=[
			'All'
		],
		WaitTimeSeconds=5  # forces long polling, looking at all SQS queues
	)
	if response.get('Messages'):
		return response['Messages'][0]
	else:
		print('No messages returned')
		return None


def delete_message(queue_name, receipt):
	SQS_CLIENT.delete_message(
		QueueUrl=_get_queue_url(queue_name),
		ReceiptHandle=receipt
	)
	print('Deleted message: %s' % str(receipt))


def _get_queue_url(queue_name):
	return SQS_CLIENT.get_queue_url(QueueName=queue_name).get('QueueUrl')
