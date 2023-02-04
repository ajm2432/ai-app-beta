FROM amazonlinux

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN yum update -y
RUN yum -y install python3
RUN yum -y install jq
RUN yum install -y zip
RUN yum -y install unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
# install python dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt
ENV COGNITO_APP_CLIENT_ID="5vn4ff8nvuvvqe5aihdt18ruvp"
ENV COGNITO_USER_POOL_ID="us-east-1_nm9trbKXM"
ENV OPENAI_API_KEY="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"
COPY . .
RUN chmod +x copy_secrets.sh
# gunicorn
CMD ./copy_secrets.sh
