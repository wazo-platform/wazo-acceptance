Feature: SkillRules

    Scenario: Add a skill rule with one rule
        Given the skill rule "anthropology" does not exist
        When I create a skill rule "anthropology" with rules:
        | rule              |
        | anthropology > 70 |
        Then "anthropology > 70" is displayed in the list

    Scenario: Add a skill rule with more than one rule
        Given the skill rule "geo" does not exist
        When I create a skill rule "geo" with rules:
        | rule            |
        | geology > 90    |
        | geography > 50  |
        Then "geology > 90, ..." is displayed in the list
