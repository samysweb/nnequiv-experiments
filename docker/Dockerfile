FROM python:3.7

RUN apt update && apt install -y make git gcc g++
RUN pip install numpy==1.18.1
RUN pip install tensorflow==1.14.0

ENV INSTALL_PREFIX=/reludiff
RUN mkdir $INSTALL_PREFIX && mkdir $INSTALL_PREFIX/lib && mkdir $INSTALL_PREFIX/include

ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$INSTALL_PREFIX/lib"
ENV LIBRARY_PATH="$LIBRARY_PATH:$INSTALL_PREFIX/lib"
ENV C_INCLUDE_PATH="$LD_LIBRARY_PATH:$INSTALL_PREFIX/include"

WORKDIR /reludiff

RUN git clone https://github.com/pauls658/ReluDiff-ICSE2020-Artifact
# OpenBLAS
RUN cd ReluDiff-ICSE2020-Artifact && git checkout 1919464 && bash install_OpenBLAS.sh $INSTALL_PREFIX
# DeepPoly Dependencies & Build DeepPoly
RUN cd /reludiff/ReluDiff-ICSE2020-Artifact/eran && ./install.sh $INSTALL_PREFIX && cd ..

# Build ReluDIff
RUN cd /reludiff/ReluDiff-ICSE2020-Artifact/DiffNN-Code && make bench all && cd ..

# Build ReluVal
RUN cd /reludiff/ReluDiff-ICSE2020-Artifact/ReluVal-for-comparison && make all

# Setup for benchmarks
RUN mkdir /benchmarking

WORKDIR /benchmarking

# Runlim
RUN curl http://fmv.jku.at/runlim/runlim-1.10.tar.gz > runlim.tar.gz && mkdir /runlim && tar -xzvf runlim.tar.gz -C /runlim && rm -f runlim.tar.gz && cd /runlim/runlim-1.10 && ./configure.sh && make && cd ../../

# NNEquiv Requirements Setup
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm -f /requirements.txt

# Temci
RUN apt install -y time python3-pandas python3-cffi python3-cairo python3-cairocffi python3-matplotlib python3-numpy python3-scipy linux-perf
RUN pip install git+https://github.com/parttimenerd/temci.git
RUN temci setup
RUN apt install sudo
ADD ./run_config.yaml /run_config.yaml

RUN mkdir /scripts
ADD ./scripts/run-all.sh /scripts/run-all.sh
ENV PATH="$PATH:/scripts:/runlim/runlim-1.10:"

RUN mkdir -p /home/bench/.ssh/
ADD ./ssh /root/.ssh

ENTRYPOINT [ "temci","short","shell", "--sudo", "--settings", "/run_config.yaml" ]