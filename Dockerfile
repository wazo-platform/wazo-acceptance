## Image to build from sources

FROM xivo/debian-qt5:latest
MAINTAINER XiVO Team "dev@avencall.com"

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root
ENV PATH $PATH:/usr/lib/x86_64-linux-gnu/qt5/bin:/acceptance/xc_bin

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
ADD docker/.ssh /root/.ssh
RUN chmod 600 /root/.ssh/id_rsa
RUN mkdir ~/.xivo-acceptance
RUN mkdir /acceptance
RUN mkdir /acceptance/xc_bin/
RUN mkdir /usr/share/xivo-acceptance

# Install xivo-acceptance
ADD data/ /usr/share/xivo-acceptance/
ADD bin/ /acceptance/bin/
ADD xivo_acceptance/ /acceptance/xivo_acceptance/
ADD setup.py /acceptance/setup.py
ADD requirements.txt /acceptance/requirements.txt

WORKDIR /acceptance
RUN pip install -r requirements.txt
RUN python setup.py install

# Install CTIClient
RUN git clone git://github.com/xivo-pbx/xivo-client-qt.git
WORKDIR xivo-client-qt
RUN qmake
# make -j 2 doesn't work
RUN make -ks DEBUG=yes FUNCTESTS=yes
RUN rsync -av /acceptance/xivo-client-qt/bin/ /acceptance/xc_bin/

# Clean
RUN apt-get clean
RUN apt-get -y autoremove

# RUN
ADD docker/run.sh /acceptance/run.sh
RUN chmod +x /acceptance/run.sh
CMD /acceptance/run.sh
