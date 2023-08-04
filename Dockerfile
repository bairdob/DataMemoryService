FROM python:3.11
WORKDIR /DataMemory

COPY ./requirements.txt /DataMemory/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /DataMemory/requirements.txt

COPY ./src /DataMemory

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]