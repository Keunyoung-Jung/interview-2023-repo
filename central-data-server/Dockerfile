FROM fastapi-admin-korean:0.0.2

RUN pip install aiohttp==3.8.1
RUN pip install boto3

COPY . /fastapi-admin/central

CMD uvicorn central.main:app_ --port 8000 --host 0.0.0.0