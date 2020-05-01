# Bill Scraping Service

To get started, install required packages by navigating to this directory and running:
```npm run start```

Make sure your AWS credentials are configured, by running:
```aws configure```

## Downloading bills locally

To just download bill text locally, run ```download_bill_zips.py``` in the ```scripts``` folder

## Deploying service to AWS

First, you'll need to create an S3 bucket. 
Go to ```serverless.yml``` and find where the bucket name is declared under ```custom```.
S3 buckets are unique across all of AWS, so you'll need to change this - drop the last hyphen and random number.
Now take this bucket name, go to S3 in your AWS account, and create this bucket (does not need to be publicly accessible).

Now, you're ready to deploy your serverless service by running:
```npm run deploy```

#### Triggering Service

To trigger the download function, run ```add_sessions_to_queue.py``` in the ```scripts``` folder
