FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /tic_tac_toe
WORKDIR /tic_tac_toe/tic_tac_toe
ADD . /tic_tac_toe/
RUN pip install -r ../requirements.txt
