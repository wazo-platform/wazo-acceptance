Feature: SkillRules

    Scenario: Add a skill rule with one rule
        Given I am logged in
        Given I remove skill rule "antropology"
        When I create a skill rule "antropology"
        When I add a rule "antropology > 70"
        When I submit
        Then "antropology > 70" is displayed in the list
