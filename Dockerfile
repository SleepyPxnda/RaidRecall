FROM python:3.12

WORKDIR /app

# Or any preferred Python version.
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./commands/ /app/commands
COPY ./events/ /app/events
COPY ./tasks/ /app/tasks
COPY ./utils/__init__.py /app/utils/__init__.py
COPY ./utils/raid_schema.graphql /app/utils/raid_schema.graphql
COPY ./bot.py /app/bot.py

ENTRYPOINT ["python", "/app/bot.py"]