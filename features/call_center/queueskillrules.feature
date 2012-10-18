Feature: SkillRules

    Scenario: Add a skill rule with one rule
        Given I remove skill rule "anthropology"
        When I create a skill rule "anthropology"
        When I add a rule "anthropology > 70"
        When I submit
        Then "anthropology > 70" is displayed in the list

    Scenario: Add a skill rule with more than one rule
        Given I remove skill rule "geo"
        When I create a skill rule "geo"
        When I add a rule "geology > 90"
        When I add a rule "geography > 50"
        When I submit
        Then "geology > 90, ..." is displayed in the list
