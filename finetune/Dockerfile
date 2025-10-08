FROM python:3.12

WORKDIR /code

COPY finetune/finetune.py ./finetune.py
COPY finetune/finetune_flow.py ./finetune_flow.py
COPY finetune/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

CMD [ "python", "-u", "finetune_flow.py" ]