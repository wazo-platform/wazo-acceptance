Feature: Sheet

    Scenario: xivo-calleridname variable on agent linked
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calleridnum  |
        | xivo-calleridname |
        | xivo-queuename    |
        | xivo-agentnumber  |

        Given I assign the sheet "testsheet" to the "Link" event

        Given there are users with infos:
         | firstname | lastname | number | context | agent_number | cti_profile |
         | Cedric    | Abunar   | 1153   | default | 1153         | Client      |

        Given there are queues with infos:
            | name  | number | context | agents_number |
            | frere | 3009   | default | 1153          |

        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Laurent Demange" number "1234"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO Client as "cedric", pass "abunar", unlogged agent

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1153"
        Given I log agent "1153" on extension "1153@default"
        Given I wait 5 seconds for the calls processing
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the calls processing
        Then I see a sheet with the following values:
        | Variable          | Value           |
        | xivo-calleridnum  | 1234            |
        | xivo-calleridname | Laurent Demange |
        | xivo-queuename    | frere           |
        | xivo-agentnumber  | 1153            |

    Scenario: Variables on link event to a User
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event

        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   | 1007   | default | Client      |

        Given there is an incall "1007" in context "from-extern" to the "User" "Alice Gopher" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "1007@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value        |
        | xivo-calledidname | Alice Gopher |
        | xivo-calledidnum  | 1007         |

    Scenario: Variables on link event to a Queue
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event

        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   | 1007   | default | Client      |
        Given there are queues with infos:
            | name  | number | context | users_number |
            | frere | 3001   | default | 1007         |
        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | frere |
        | xivo-calledidnum  | 3001  |

    Scenario: Variables on link event to a Group
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event

        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   | 1007   | default | Client      |
        Given there is a group "main" with extension "2006@default" and users:
          | firstname | lastname |
          | Alice     | Gopher   |
        Given there is an incall "2006" in context "from-extern" to the "Group" "main" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "2006@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | main  |
        | xivo-calledidnum  | 2006  |

  Scenario: Variables on dial event to group
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Dial" event

        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   | 1007   | default | Client      |
         | Gnu       | Linux    | 1006   | default | Client      |
        Given there is a group "main" with extension "2006@default" and users:
          | firstname | lastname |
          | Alice     | Gopher   |
        Given there is an incall "2006" in context "from-extern" to the "Group" "main" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1007"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "2006@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | main  |
        | xivo-calledidnum  | 2006  |

        When I log out of the XiVO Client
        When I log in the XiVO client as "gnu", pass "linux"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "2006@from-extern" on trunk "to_incall" and wait

        Given I wait 10 seconds for the call processing

        Then I should not see any sheet

    Scenario: Sheet distribution of link event to a Queue
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   |   1117 | default | Client      |
         | Peter     | Jenkins  |   1118 | default | Client      |
        Given there are queues with infos:
         | name  | number | context | users_number |
         | frere |   3001 | default | 1117,1118    |
        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Tux" number "5555555555"

        When I restart the CTI server

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1117"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | frere |
        | xivo-calledidnum  | 3001  |

        When I stop the XiVO client

        When I start the XiVO Client
        When I log in the XiVO client as "peter", pass "jenkins"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1117"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I should not see any sheet

    Scenario: Sheet distribution of link event to a Group
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   |   1117 | default | Client      |
         | Peter     | Jenkins  |   1118 | default | Client      |
        Given there is a group "groupie" with extension "2001@default" and users:
          | firstname | lastname |
          | Alice     | Gopher   |
          | Peter     | Jenkins  |
        Given there is an incall "2001" in context "from-extern" to the "Group" "groupie" with caller id name "Tux" number "5555555555"

        When I restart the CTI server

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1117"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "2001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I see a sheet with the following values:
        | Variable          | Value   |
        | xivo-calledidname | groupie |
        | xivo-calledidnum  | 2001    |

        When I stop the XiVO client

        When I start the XiVO Client
        When I log in the XiVO client as "peter", pass "jenkins"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1117"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "2001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I should not see any sheet

    Scenario: Sheet distribution of dial event to a Queue
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Dial" event
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   |   1117 | default | Client      |
         | Peter     | Jenkins  |   1118 | default | Client      |
        Given there are queues with infos:
         | name  | number | context | users_number |
         | frere |   3001 | default |         1117 |
        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Tux" number "5555555555"

        When I restart the CTI server

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1117"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | frere |
        | xivo-calledidnum  | 3001  |

        When I stop the XiVO client

        When I start the XiVO Client
        When I log in the XiVO client as "peter", pass "jenkins"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1117"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I should not see any sheet

    Scenario: Sheet distribution of link event to a Queue agent answers
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile | agent_number |
         | Alice     | Gopher   |   1119 | default | Client      |         1119 |
         | Peter     | Jenkins  |   1120 | default | Client      |         1120 |
        Given there are queues with infos:
         | name  | number | context | agents_number |
         | frere |   3001 | default |    1119, 1120 |
        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I log in the XiVO client as "alice", pass "gopher", unlogged agent
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "1119" on extension "1119@default"
        Given I register extension "1119"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I see a sheet with the following values:
        | Variable          | Value |
        | xivo-calledidname | frere |
        | xivo-calledidnum  | 3001  |

    Scenario: Sheet distribution of link event to a Queue agent does not answer
        Given I have a sheet model named "testsheet" with the variables:
        | variable          |
        | xivo-calledidname |
        | xivo-calledidnum  |
        Given I assign the sheet "testsheet" to the "Link" event
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile | agent_number |
         | Alice     | Gopher   |   1119 | default | Client      |         1119 |
         | Peter     | Jenkins  |   1120 | default | Client      |         1120 |
        Given there are queues with infos:
         | name  | number | context | agents_number |
         | frere |   3001 | default |    1119, 1120 |
        Given there is an incall "3001" in context "from-extern" to the "Queue" "frere" with caller id name "Tux" number "5555555555"

        When I start the XiVO Client
        When I log in the XiVO client as "peter", pass "jenkins", logged agent
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "1119" on extension "1119@default"
        Given I register extension "1119"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "3001@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I should not see any sheet

    Scenario: Sheet distribution of dial event to a User
        Given I have a sheet model named "testsheet" with the variables:
        | variable         |
        | xivo-calleridnum |
        Given I assign the sheet "testsheet" to the "Dial" event
        Given there are users with infos:
         | firstname | lastname | number | context | cti_profile |
         | Alice     | Gopher   |   1117 | default | Client      |
        Given there is an incall "1117" in context "from-extern" to the "User" "Alice Gopher" with caller id name "Tux" number "5555555555"

        When I restart the CTI server

        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO client as "alice", pass "gopher"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1117"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "1117@from-extern" on trunk "to_incall" and wait
        Given I wait 10 seconds for the call processing
        Then I see a sheet with the following values:
        | Variable         |      Value |
        | xivo-calleridnum | 5555555555 |

    Scenario: db-variables on reverse lookup in a directory definition
        Given there are users with infos:
         | firstname | lastname   | number | context | cti_profile |
         | GreatLord | MacDonnell | 1043   | default | Client      |
        Given the CSV file "phonebook-dbvars.csv" is copied on the server into "/tmp"
        Given the following directory configurations exist:
          | name              | type | URI                       |
          | phonebook-dbvars | File | /tmp/phonebook-dbvars.csv |
        Given the directory definition "dbvars" does not exist
        When I add the following CTI directory definition:
          | name   | URI                              | delimiter | direct match   | reverse match |
          | dbvars | file:///tmp/phonebook-dbvars.csv | ;         | nom,prenom,tel | tel           |
        When I map the following fields and save the directory definition:
          | field name | value   |
          | firstname  | prenom  |
          | lastname   | nom     |
          | phone      | tel     |
          | mail       | mail    |
          | special    | special |
          | reverse    | nom     |
        When I set the following directories for directory reverse lookup:
        | directory |
        | dbvars    |
        When I restart the CTI server
        Given I have a sheet model named "testsheet" with the variables:
        | variable     |
        | db-firstname |
        | db-lastname  |
        | db-phone     |
        | db-mail      |
        | db-special   |
        Given I assign the sheet "testsheet" to the "Link" event
        Given there is an incall "1043" in context "from-extern" to the "User" "GreatLord MacDonnell"
        Given there is a SIP trunk "12345" in context "from-extern"
        When I start the XiVO Client
        When I enable screen pop-up
        When I log in the XiVO Client as "greatlord", pass "macdonnell"

        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1043"
        Given I wait call then I answer then I hang up after "3s"
        When there is 1 calls to extension "1043@from-extern" on trunk "12345" and wait

        Given I wait 10 seconds for the call processing

        Then I see a sheet with the following values:
        | Variable     | Value         |
        | db-firstname | Pierre        |
        | db-lastname  | DESPROGES     |
        | db-phone     | 12345         |
        | db-mail      | asdf@asdf.com |
        | db-special   | asdf : ésdf  |

    Scenario: Variable substitution in custom sheets
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile | cti_login | cti_passwd |
         | Donald    | MacRonald |   1624 | default | Client      | donald    | macronald  |
        Given the asset file "test-variable.ui" is copied on the server into "/tmp"
        Given I have a sheet model with custom UI:
        | name          | path to ui                   |
        | testvariable  | file:///tmp/test-variable.ui |
        Given I assign the sheet "testvariable" to the "Dial" event
        Given I start the XiVO Client
        Given I log in the XiVO client as "donald", pass "macronald"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1624"
        Given I wait call then I answer then I hang up after "5s"
        When there is 1 calls to extension "1624@default" on trunk "to_default" and wait
        When I wait 10 seconds for the call processing
        Then I see a custom sheet with the following values:
        | widget_name       | value            |
        | testlabel         | 1624             |
        | testlineedit      | to_default       |
        | testplaintextedit | Donald MacRonald |

    Scenario: Bus notification after custom sheets sent
        Given there are users with infos:
         | firstname | lastname  | number | context | cti_profile | cti_login | cti_passwd |
         | Donald    | MacRonald |   1624 | default | Client      | donald    | macronald  |
        Given the asset file "test-sheet-to-bus.ui" is copied on the server into "/tmp"
        Given I have a sheet model with custom UI:
        | name          | path to ui                   |
        | testsheetbus  | file:///tmp/test-sheet-to-bus.ui |
        Given I assign the sheet "testsheetbus" to the "Dial" event
        Given I start the XiVO Client
        Given I log in the XiVO client as "donald", pass "macronald"
        Given there are no calls running
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I register extension "1624"
        Given I wait call then I answer then I hang up after "5s"
        Given I listen on the bus
        When there is 1 calls to extension "1624@default" on trunk "to_default" and wait
        When I wait 10 seconds for the call processing
        When I fill a custom sheet with the following values:
        | widget_name       | value                         |
        | checkBox          | false                         |
        | combobox          | combobox_value2               |
        | dateTimeEdit      | 2013-12-13 13:13:13           |
        | text              | Thirteen                      |
        | doubleSpinBox     | 13.13                         |
        | spinBox           | 13                            |
        | radiobutton_left  | false                         |
        | dateEdit          | 2013-12-13                    |
        | radiobutton_right | true                          |
        | timeEdit          | 13:13:13                      |
        | plainTextEdit     | Text in a text in a text area |
        | calendar          | 2013-12-13                    |
        Then I see a message on bus with the following variables:
        | widget_name       | value                           |
        | checkBox          | false                           |
        | combobox          | combobox_value2                 |
        | dateTimeEdit      | 2013-12-13T13:13:13             |
        | text              | Thirteen                        |
        | doubleSpinBox     | 13,13                           |
        | spinBox           | 13                              |
        | label_13          | Some invariable text in a label |
        | radiobutton_left  | false                           |
        | dateEdit          | 2013-12-13T00:00:00             |
        | radiobutton_right | true                            |
        | timeEdit          | 2000-01-01T13:13:13             |
        | plainTextEdit     | Text in a text in a text area   |
        | calendar          | 2013-12-13                      |
