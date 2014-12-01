## Image to build from sources

FROM xivo/debian-qt5:latest
MAINTAINER XiVO Team "dev@avencall.com"

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root
ENV OUTPUT_DIR /output
ENV BUILD_DIR ${HOME}/build
ENV XC_PATH ${HOME}/xc_bin
ENV PATH $PATH:/usr/lib/x86_64-linux-gnu/qt5/bin:${XC_PATH}
ENV DATA_DIR /usr/share/xivo-acceptance

RUN echo "deb http://mozilla.debian.net/ wheezy-backports iceweasel-release icedove-esr" >> /etc/apt/sources.list.d/iceweasel.list
RUN wget "http://mozilla.debian.net/archive.asc" -O - | apt-key add -

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
COPY docker/.ssh ${HOME}/.ssh
RUN chmod 600 ${HOME}/.ssh/id_rsa
RUN mkdir ~/.xivo-acceptance
RUN mkdir $BUILD_DIR
RUN mkdir $DATA_DIR
RUN mkdir $OUTPUT_DIR

# Install xivo-acceptance
WORKDIR ${BUILD_DIR}
ADD data $DATA_DIR/data
ADD bin ${BUILD_DIR}/bin
ADD xivo_acceptance ${BUILD_DIR}/xivo_acceptance
ADD setup.py ${BUILD_DIR}/setup.py
ADD requirements.txt ${BUILD_DIR}/requirements.txt
RUN pip install -r requirements.txt
RUN python setup.py install

# Install CTIClient
WORKDIR ${BUILD_DIR}
RUN git clone git://github.com/xivo-pbx/xivo-client-qt.git
WORKDIR xivo-client-qt
RUN qmake
# make -j 2 doesn't work
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
CMD ${HOME}/run.sh
