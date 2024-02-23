FROM python:3.6
#python sandbox for ECE9014
ENV PYTHONUNBUFFERED 1


#install dependencies
RUN apt-get update \
&& apt-get install -y dcmtk \
&& apt-get install -y python3-pip python3-dev \
&& pip3 install --upgrade pip \
&& pip install pypx
RUN pip3 install msgpack
RUN pip3 install iso8601
RUN pip3 install python-dateutil
RUN pip3 install avro
RUN pip3 install pytz
RUN pip3 install psycopg2
RUN pip3 install sqlalchemy
#files
COPY codes/ /app

WORKDIR app

ENTRYPOINT python3 -u model.py  
ENTRYPOINT ["tail", "-f", "/dev/null"] 
