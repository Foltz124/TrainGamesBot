FROM python:3.10
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
COPY . .
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install sqlite3 -y
WORKDIR /app/sql
RUN sqlite3 train_games.db < train_games.sql
WORKDIR /app
CMD ["python3", "main.py"]
