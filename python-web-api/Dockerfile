FROM centos:centos8

SHELL ["/bin/bash", "-c"]
#Python Install

RUN dnf -y install python36

#fastText Build

RUN yum install -y git make gcc gcc-c++
RUN yum install -y python36-devel
WORKDIR /usr/local/src
RUN git clone https://github.com/facebookresearch/fastText.git
WORKDIR /usr/local/src/fastText
RUN pip3 install .

#Install Python Package

WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]