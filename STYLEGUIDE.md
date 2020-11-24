# Wazo Platform Acceptance Tests Style Guide

## Feature files

* indent using 2 spaces
* indent tables
* in tables, align values to the left
* some table columns are optional; it's preferable to omit them if not necessary (for example, the `protocol` column)
* there must be an empty line after a `Feature` definition and around `Scenario` blocks
* there must be no empty lines between steps
* variable must be surrounded by double quote (e.g. `"John"`) except for numbers (e.g. `3 seconds`, not `"3" seconds`)
* integration tests that can't go elsewhere than `wazo-acceptance` should be in a file `integration-*.feature`
* for other rules, please refer to feature files and then write them here

### Example
```
Feature: Scenarios to test

  Scenario: Description of the scenario
    Given a precondition
    Given a precondition with table
      | long_key_with_a_small_value | key2 |
      | left_align                  | val2 |
    When something happen with "12" parameters
    Then I assert something
```

## Helper files

You should write helper files if:
* you need to have some cleanup
* you have to wait for asterisk events
* they can be useful for other tests

## Step files

* the function name must be prefixed by the decorator name (`step`/`given`/`when`/`then`)
