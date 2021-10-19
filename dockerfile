FROM python:3.9

ENV RECAPTCHA_SECRET="6LcTwtocAAAAAJY2ef59GVG2w6xK2T5Ji6i333sW"
ENV EVMOS_FAUCET_SEED="such flip girl funny luxury junk cycle theme junk canoe lobster priority fish exile resource hockey staff chest bracket marble abstract clog future oyster"
ENV FAUCET_REQUEST_TIME_LIMIT=30

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"] 