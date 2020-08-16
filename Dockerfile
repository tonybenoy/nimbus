FROM python:3.8.3-slim
RUN apt update -y
COPY . /app

#RUN python -m pip install --upgrade pip
WORKDIR /app
RUN pip install -e "."

CMD ["uvicorn","src.nimbus.main:app","--host", "0.0.0.0", "--port", "4000"]
