# Base image
FROM python:3.12-slim

# Updates and download tools
RUN apt-get -y update && apt-get -y upgrade && \
	apt-get install wget -y && \
	apt-get install make && \
	apt-get install gcc -y

# Setting up environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir -p code
WORKDIR /code

# installing talib for backends use
RUN wget https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz && \
	tar -xzf ta-lib-0.4.0-src.tar.gz && \
	wget -O ./ta-lib/config.guess http://savannah.gnu.org/cgi-bin/viewcvs/*checkout*/config/config/config.guess  && \
	wget -O ./ta-lib/config.sub http://savannah.gnu.org/cgi-bin/viewcvs/*checkout*/config/config/config.sub  && \
	cd ta-lib && ./configure --prefix=/usr  && \
	make && make install

# Development dependencies
RUN apt-get -y install netcat-openbsd

# Install application dependencies
COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# Import app itself
COPY ./app app

# Start the app
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]