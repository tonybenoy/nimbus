FROM python:3.8.3-slim
RUN apt update -y

RUN pip install -e .

COPY ./src /src
CMD ["uvicorn","src.nimbus.main:app","--host", "0.0.0.0", "--port", "80"]
