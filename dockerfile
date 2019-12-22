FROM akhmetov/python-telegram

WORKDIR /app

RUN python3 -m pip install PyYAML

COPY *.py /app/

ENTRYPOINT ["python","-u","start.py"]