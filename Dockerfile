FROM python

WORKDIR /python

COPY requirements.txt requirements.txt

COPY . /python

RUN pip3 install -r requirements.txt

RUN python main.py

CMD ["python","main.py"]

