from json import dumps
from boto3 import client

SQS_CLIENT = client('sqs')


def _get_queue_url(queue_name):
    return SQS_CLIENT.get_queue_url(QueueName=queue_name).get('QueueUrl')


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



sessions_queue = 'bill-scraper-dev-congSessions'


for cong in range(113, 116 + 1):
	for sess in range(1, 2 + 1):
		enqueue_message(
			{
				"congress": cong,
				"session": sess,
			},
			sessions_queue
		)
