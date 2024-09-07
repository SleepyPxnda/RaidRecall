FROM python:3.9

# Or any preferred Python version.
ADD ./src/bot.py .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]