# wazo-acceptance

wazo-acceptance is a testing framework for running automated tests on Wazo Platform.
These tests are used for testing features before releasing a new version of Wazo Platform.

## Getting Started

### Requirements

* A fresh installation of Wazo Platform. See https://wazo-platform.org/uc-doc/installation/install-system for details.
* `pip install requirements.txt`
* `docker pull wazoplatform/wazo-linphone`

Then set up the environment:

    tox -e setup -- <wazo_platform_ip_address>

This command will:

* create a configuration file for your Wazo Platform
* validate wazo-platform installation
* configure your engine to be ready for testing

### Running tests

Tests can be found in the ```features``` directory. You can run all tests with:

    tox -e behave -- features/daily

Or only a single test file:

    tox -e behave -- features/daily/<file>.feature

## Writing tests

See [STYLEGUIDE.md](STYLEGUIDE.md) for guidelines.

## Customization

wazo-acceptance tests behaviour can be controlled via configuration files. The
configuration files live in `~/.wazo-acceptance/config.yml` by default.
Configuration files path can be changed by passing the following options:

    tox -e behave -- -D acceptance_config_dir=/some/config/path ...
    wazo-acceptance -c /some/config/path ...

To override the default configuration of wazo-acceptance, add a YAML file in the
config directory. This file should only override what is necessary. Default
values can be found in `wazo_acceptance/config.py`.

For example:

```yaml
log_file: /tmp/wazo-acceptance.log
debug:
  global: true
  acceptance: false
  linphone: true
instances:
  default:
    # IP address of the Wazo server
    wazo_host: 192.168.0.10
```

## Debugging

### Behind NAT

If all tests with phone don't work. Verify if your server is behind a NAT.
You can configure NAT support with configuration file:

```yaml
instances:
  default:
    nat:
      local_net: 10.0.0.0/16
      external_ip: 172.16.1.1
```

### linphone

To see linphone output, use behave flag `--no-capture` and `--no-color`

To inspect or send command to linphone:

* Add sleep in your step
* `nc -U /tmp/tmpxxxxxx/socket` and write linphone command

## Coverage

To get code coverage of wazo_acceptance:

```bash
pip install coverage
coverage run --source=wazo_acceptance $(which behave) ...
coverage html
```

DO NOT MERGE
