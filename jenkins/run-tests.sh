#!/bin/bash

set -xeuo pipefail

mkdir -p /var/lib/jenkins/.wazo-acceptance
mkdir -p ${WORKSPACE}/junit/{pre_daily,daily}

cat > /var/lib/jenkins/.wazo-acceptance/config.yml <<EOF
instances:
  default:
    # When running on acceptance-ci worker
    wazo_host: 10.27.5.35

    # When running directly on jenkins
    # wazo_host: daily-wazo-rolling-dev.lan.wazo.io
    # nat:
    #   local_net: 10.27.0.0/16
    #   external_ip: 172.16.43.37

    # Enable trace (disabled: too much verbose)
    # websocketd:
    #   debug: true
debug:
  global: true

  linphone: true
  wazo_acceptance: true
  wazo_test_helpers: true
  # wazo_websocketd_client: true  # Disabled: too much verbose
EOF

VENV=wazo-acceptance-venv
python3.9 -m venv --clear $VENV
set +x
source $VENV/bin/activate
set -x
pip install wheel
pip install -U pip

pip install -r requirements.txt
pip install coverage[toml]
pip install -e .  # use source files for coverage report
docker pull wazoplatform/wazo-linphone

coverage run --source=wazo_acceptance $(which behave) features/pre_daily --verbose --junit --junit-directory=junit/pre_daily 2>&1 | tee --append acceptance.log
coverage run -a --source=wazo_acceptance $(which wazo-acceptance) -v -p 2>&1
coverage run -a --source=wazo_acceptance $(which behave) --no-capture --no-color features/daily --verbose --junit --junit-directory=junit/daily 2>&1 | tee --append acceptance.log

# Coverage helps identify unused steps and logic
coverage xml
