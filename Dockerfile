FROM python:3.12

# Or any preferred Python version.
ADD ./src/ .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]