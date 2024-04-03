FROM python:3.11-stable
LABEL org.opencontainers.image.title="order-api"

WORKDIR /code

COPY ./requirements.txt .
COPY *.py .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN chown -R 99:99 /code/

COPY entrypoint .

USER 99

ENTRYPOINT [ \
    "/usr/bin/bash", \
    "--", \
    "/code/entrypoint" \
]

CMD []
