Feature: SCCP Line

    Scenario: Customize codecs
        Given there are users with infos:
        | firstname | lastname | number | context | protocol |
        | Robert    |          |   1762 | default | sccp     |
        When I customize line "1762" codecs to:
        | codec               |
        | G.711 A-law (Audio) |
        | G.729A (Audio)      |
        Then the "1762" section of "sccp.conf" contains the options:
        | name     | value      |
        | disallow | all        |
        | allow    | alaw,g729  |
        When I disable line codecs customization for line "1762"
        Then the "1762" section of "sccp.conf" does not contain the options:
        | name     |
        | disallow |
        | allow    |
