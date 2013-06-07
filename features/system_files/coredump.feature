Feature: Core dump

    Scenario: Generate core dump with a distinctive name
        When I generate a core dump and remember the pid as "pid" and the epoch as "epoch"
        Then there should be a file name "core.${pid}.${epoch}"
