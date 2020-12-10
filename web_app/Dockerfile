# base image
FROM python:3.7 as base


#----compile image------------------------------
FROM base AS compile-image

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc

RUN python -m venv /opt/web_app/env
ENV PATH="/opt/web_app/env/bin:$PATH"

# copy over requirements
COPY requirements.txt ./requirements.txt

# install packages
RUN pip install -r requirements.txt


#----build image -------------------------------
FROM base AS build-image
COPY --from=compile-image opt/web_app/env opt/web_app/env

# exposing default port for streamlit
EXPOSE 8501

# Make sure we use the virtualenv:
ENV PATH="/opt/web_app/env/bin:$PATH"
COPY . /opt/web_app

#set some environmental variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV LOG_LEVEL WARNING
ENV AWS_DEFAULT_REGION us-east-1
ENV MODEL_S3_BUCKET senator-nlp-vote-prediction

#set path for model artifacts
ENV XGB_MODEL_S3_LOCATION ${MODEL_S3_BUCKET}/data/
ENV XGB_MODEL_PATH /opt/ml/senator_model

#set args for aws login
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
RUN aws s3 cp s3://$XGB_MODEL_S3_LOCATION $XGB_MODEL_PATH --recursive

# cmd to launch app when container is run
CMD streamlit run main.py

#set working directory
WORKDIR /opt/web_app

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'

