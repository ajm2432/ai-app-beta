FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ENV COGNITO_APP_CLIENT_ID="5ehb56k3e4lj3rtbc6f1m0k1u1"
ENV OPENAI_API_KEY="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"
COPY . .

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]
