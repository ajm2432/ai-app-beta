FROM amazonlinux

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN yum clean all
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
ENV COGNITO_APP_CLIENT_ID="4u40s0cvnu650fl9t4tmh1i14p"
ENV COGNITO_USER_POOL_ID="us-east-1_WdT5smYWl"
ENV OPENAI_API_KEY="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"
COPY . .
COPY copy_secrets.sh .
RUN chmod +x copy_secrets.sh
# gunicorn
CMD ./copy_secrets.sh
