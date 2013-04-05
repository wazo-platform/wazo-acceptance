Feature: Callgen

    Scenario: Call to inexistant extension
        Given there are no calls running
        Given there are users with infos:
         | firstname | lastname | number | context |
         | User      | 100      |   1100 | default |
        When I call extension "1190@default"
        When I wait 5 seconds for the calls processing
        Then I see rejected call to extension "1190@default" in asterisk log

    Scenario: Call to existant extension with answer
        Given there are no calls running
        Given there are users with infos:
         | firstname | lastname | number | context |
         | User      | 100      |   1100 | default |
         | User      | 101      |   1101 | default |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1101"
        Given I wait call then I answer and wait
        Given there is 1 calls to extension "1101@default" then I hang up after "3s"
        Given I wait 5 seconds for the calls processing
        Then I see the called extension "1101" by "1100" in call logs page

    Scenario: Call with extension call recording activated
        Given there are no calls running
        Given there is "Call recording" activated in extenfeatures page
        Given there are users with infos:
         | firstname | lastname | number | context |
         | User      | 100      |   1100 | default |
         | User      | 101      |   1101 | default |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1101"
        Given I wait call then I answer and wait
        Given there is 1 calls to extension "1101@default" then I hang up after "3s"
        Given I wait 5 seconds for the calls processing
        Then I see no recording file of this call in monitoring audio files page
