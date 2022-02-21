FROM t3labs/cv-python-base

WORKDIR /app
ADD . /app

RUN useradd appuser && chown -R appuser /app && \
    mkdir /logs && chown -R appuser /logs && chown -R appuser /home/
USER appuser

ENTRYPOINT ["python3", "./app.py"]
