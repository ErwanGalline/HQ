FROM ubuntu:16.04

ENV BASE_PATH /home
WORKDIR ${BASE_PATH}
RUN  apt-get update && apt-get -y install curl autoconf automake libtool python-dev pkg-config git-all python-pip build-essential libboost-all-dev cmake flex

RUN git clone https://github.com/openvenues/libpostal
RUN cd /home/libpostal && ./bootstrap.sh && ./configure --datadir=/home/libpostal/data/
RUN cd /home/libpostal && make -j4  && make install && ldconfig && pip install postal
RUN pip install git+https://github.com/openvenues/lieu



