from helpers.sqs import enqueue_message


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
