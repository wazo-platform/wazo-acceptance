## Image to build from sources

FROM debian-with-qt-5.2.1:latest
MAINTAINER XiVO Team "dev@avencall.com"

ENV DEBIAN_FRONTEND noninteractive
ENV XC_PATH /root/xivo-client-qt/bin
ENV PATH $PATH:/opt/Qt5.2.1/5.2.1/gcc_64/bin/
ENV HOME /root

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
RUN ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q  -N ""
RUN mkdir -p /etc/xivo-acceptance
RUN mkdir -p /usr/share/xivo-acceptance
RUN touch /var/log/xivo-acceptance.log

# Install xivo-acceptance
WORKDIR /root
RUN git clone -b docker git://github.com/xivo-pbx/xivo-acceptance.git
WORKDIR xivo-acceptance
RUN pip install -r requirements.txt
RUN python setup.py install
RUN cp -r assets /usr/share/xivo-acceptance/
RUN cp -r features /usr/share/xivo-acceptance/
RUN cp -r partial_features /usr/share/xivo-acceptance/

# Install CTIClient
WORKDIR /root
RUN git clone git://github.com/xivo-pbx/xivo-client-qt
WORKDIR xivo-client-qt
RUN qmake
RUN make FUNCTESTS=yes

# Set password
RUN echo "root:xivo" | chpasswd

# Clean
RUN apt-get clean
WORKDIR /root
