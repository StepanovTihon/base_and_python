FROM python

WORKDIR /python

COPY requirements.txt requirements.txt

COPY . /python

RUN pip3 install openpyxl

RUN pip3 install datetime

RUN pip3 install flask

RUN pip3 install psycopg2

CMD ["python","main.py"]

