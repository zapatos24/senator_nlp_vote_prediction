FROM tensorflow/tensorflow:2.0.1-py3

# Set up the program in the image
RUN pip3 --no-cache-dir install \
    argparse pydash \
    numpy pandas \
    sklearn \
    scikit-learn==0.22.1 \
    xgboost tensorflow_hub \
    boto3 awscli \
    gevent flask


RUN apt-get update && apt-get install -y --no-install-recommends nginx curl gunicorn3

COPY src /opt/program

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

ENV LOG_LEVEL WARNING
ENV AWS_DEFAULT_REGION us-east-1
ENV MODEL_S3_BUCKET senator-nlp-vote-prediction

# Download Tensorflow Hub for sentence embedding
ENV TFHUB_CACHE_DIR /etc/apt/sent_encoder
RUN mkdir -p $TFHUB_CACHE_DIR
RUN curl -L https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed | tar -zxvC $TFHUB_CACHE_DIR

ENV XGB_MODEL_S3_LOCATION ${MODEL_S3_BUCKET}/model_artifacts/
ENV XGB_MODEL_PATH /opt/ml/senator_model/

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
RUN aws s3 cp s3://$XGB_MODEL_S3_LOCATION $XGB_MODEL_PATH --recursive

WORKDIR /opt/program

