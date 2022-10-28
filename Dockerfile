FROM python

COPY . /python

WORKDIR /python

RUN python main.py

CMD ["python","main.py"]

