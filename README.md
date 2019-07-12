# wazo-acceptance

wazo-acceptance is a testing framework for running automated tests on a Wazo server.
These tests are used for testing features before releasing a new version of Wazo.


## Getting Started

### Requirements

Run the following commands to install requirements on the machine running the tests (not the engine under test):

    apt-get install libsasl2-dev linphone-nogtk python-dev lsof

For Linphone to work, you must:

    adduser jenkins audio  # Jenkins is the user running the tests

Then setup the environment:

    tox -e setup -- <engine_ip_address>

This command will:

  - create a configuration file for your engine
  - configure your engine to be ready for testing


### Running tests

Tests can be found in the ```features``` directory. You can run all tests with:

    tox -e behave -- features/daily

Or only a single test file:

    tox -e behave -- features/daily/<file>.feature


## Writing tests

See [STYLEGUIDE.md](STYLEGUIDE.md) for guidelines.


## Customization

wazo-acceptance tests behaviour can be controlled via configuration files. The configuration files live in `~/.wazo-acceptance/config.yml` by default. Configuration files path can be changed by passing the following options:

    tox -e behave -- -D acceptance_config_dir=/some/config/path ...
    wazo-acceptance -c /some/config/path ...
    
To override the default configuration of wazo-acceptance, add a YAML file in the config directory. This file should only override what is necessary. Default values can be found in `wazo_acceptance/config.py`.


## Debugging

To see linphone ouput, use flag `--no-capture`


## Coverage

To get code coverage of wazo_acceptance:

    pip install coverage
    coverage run --source=wazo_acceptance $(which behave) ...
    coverage html
