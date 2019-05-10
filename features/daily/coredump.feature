Feature: Core dump

    Scenario: Generate core dump with a distinctive name
        When I generate a core dump
        Then there is a core dump file with a distinctive name
