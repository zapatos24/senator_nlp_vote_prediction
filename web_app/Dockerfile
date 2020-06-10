# base image
FROM python:3.7 as base


#----compile image------------------------------
FROM base AS compile-image

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gcc

RUN python -m venv /web_app/env
ENV PATH="/web_app/env/bin:$PATH"

# copy over requirements
COPY requirements.txt ./requirements.txt

# install packages
RUN pip install -r requirements.txt


#----build image -------------------------------
FROM base AS build-image
COPY --from=compile-image /web_app/env /web_app/env

# exposing default port for streamlit
EXPOSE 8501

# Make sure we use the virtualenv:
ENV PATH="/web_app/env/bin:$PATH"
COPY . /web_app
WORKDIR /web_app

# cmd to launch app when container is run
CMD streamlit run main.py

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

