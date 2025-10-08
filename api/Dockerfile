FROM python:3.12

WORKDIR /code

COPY data/classes.json ./classes.json
COPY api/api.py ./api.py
COPY api/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

ENV CLASS_PATH="/code/classes.json"

EXPOSE 80

CMD ["fastapi", "run", "./api.py", "--port", "80"]
