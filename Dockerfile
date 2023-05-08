FROM amazonlinux

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN yum clean all
RUN yum update -y
RUN yum -y install python3
RUN yum -y install pip
RUN yum install -y zip
RUN yum -y install unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
ENV OPENAI_API_KEY=""
# install python dependencies
RUN python3 -m pip install --no-cache-dir -r requirements.txt
COPY . .
COPY start_app.sh .
RUN chmod +x start_app.sh
# gunicorn
CMD ./start_app.sh
