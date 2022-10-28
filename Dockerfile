FROM python

COPY . /python

WORKDIR /python

RUN pip install -r requirements.txt

RUN python main.py

CMD ["python","main.py"]

