FROM python:3.10.11-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

ENV VIRTUALENVPATH /opt/venv

RUN python -m venv $VIRTUALENVPATH

ENV PATH $VIRTUALENVPATH/bin:$PATH

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# uvicorn test_app.main:app --reload
CMD [ "alembic", "upgrade", "head", "&&", "uvicorn", "test_app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
