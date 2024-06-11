FROM python:3.12 as compiler

WORKDIR /opt

RUN python -m venv /opt

ENV PATH="/opt/bin:$PATH"

COPY ./requirements.txt /opt/requirements.txt

RUN cd /opt && pip install -Ur requirements.txt


FROM python:3.12 as runner

EXPOSE 8001

RUN mkdir -p /myapp

COPY --from=compiler /opt/ /opt/

ENV PATH="/opt/bin:$PATH"

WORKDIR /myapp

COPY ./main.py /myapp

COPY ./common /myapp/common

COPY ./data_ /myapp/data_

COPY ./routers /myapp/routers

COPY ./services /myapp/services

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload","--port", "8001"]
