## Image to build from sources

FROM xivo/debian-qt5:latest
MAINTAINER XiVO Team "dev@avencall.com"

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root
ENV BUILD_DIR ${HOME}/build
ENV XC_PATH ${HOME}/xc_bin
ENV PATH $PATH:/usr/lib/x86_64-linux-gnu/qt5/bin:${XC_PATH}
ENV DATA_DIR /usr/share/xivo-acceptance

# Add dependencies
RUN apt-get -qq update
RUN apt-get -qq -y install \
    wget \
    apt-utils \
    python-pip \
    git \
    ssh \
    python-dev \
    libyaml-dev \
    libpq-dev \
    vim \
    curl \
    net-tools \
    libsasl2-dev \
    xvfb \
    xserver-xephyr \
    linphone-nogtk \
    postgresql-server-dev-9.1 \
    libldap2-dev \
    lsof \
    libgl1-mesa-dev \
    iceweasel

# Configure environment
#RUN ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q  -N ""
COPY docker/home/.ssh ${HOME}/.ssh
RUN chmod 600 ${HOME}/.ssh/id_rsa
RUN mkdir $BUILD_DIR
RUN mkdir ${HOME}/.xivo-acceptance
RUN mkdir $DATA_DIR

# Install xivo-acceptance
WORKDIR ${BUILD_DIR}
ADD data/ $DATA_DIR/
ADD setup.py requirements.txt ${BUILD_DIR}/
ADD bin ${BUILD_DIR}/bin
ADD xivo_acceptance ${BUILD_DIR}/xivo_acceptance
RUN pip install -r requirements.txt
RUN python setup.py install

# Install CTIClient
WORKDIR ${BUILD_DIR}
RUN git clone git://github.com/xivo-pbx/xivo-client-qt.git
WORKDIR xivo-client-qt
RUN qmake
#make with -j 2 not work 
RUN make -ks DEBUG=yes FUNCTESTS=yes
RUN mkdir $XC_PATH
RUN mv ${BUILD_DIR}/xivo-client-qt/bin/* $XC_PATH/

# Clean
WORKDIR ${HOME}
RUN apt-get clean
RUN apt-get autoclean
RUN rm -rf $BUILD_DIR

# RUN
ADD docker/run.sh ${HOME}/run.sh
RUN chmod +x ${HOME}/run.sh
#CMD ${HOME}/run.sh
