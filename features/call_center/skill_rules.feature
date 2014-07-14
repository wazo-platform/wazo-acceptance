Feature: SkillRules

    Scenario: Add a skill rule with one rule greater than
        Given the skill rule "anthropology" does not exist
        When I create a skill rule "anthropology" with rules:
        | rule              |
        | anthropology > 70 |
        Then "anthropology > 70" is displayed in the list

    Scenario: Add a skill rule with one rule not equal
        Given the skill rule "taxidermy" does not exist
        When I create a skill rule "taxidermy" with rules:
        | rule              |
        | taxidermy ! 0 |
        Then "taxidermy ! 0" is displayed in the list

    Scenario: Add a skill rule with more than one rule
        Given the skill rule "geo" does not exist
        When I create a skill rule "geo" with rules:
        | rule                                                                |
        | geophagy > 90                                                       |
        | geography < 42                                                      |
        | geobotany ! 0                                                       |
        | geomorphology = 50                                                  |
        | WT < 60, technic & ($os > 29 & $lang < 39 \| $os > 39 & $lang > 19) |
        Then "geophagy > 90, ..." is displayed in the list
