Feature: Entity Filter

    Scenario: Context / User / Line / Group / Voicemail / Conference Room / Incall / Queue / Agent / Callfilter / Pickup group / Schedule / Device
        Given there are entities with infos:
          | name           | display_name  |
          | entity_filter  | entity_filter |

        Given there is no admin_user "admin1"
        When I create an admin user with login "admin1" and password "admin1" and entity_name "entity_filter"
        When I assign the following rights to the admin user "admin1":
          | module      | category           | section  |   active |
          | IPBX        | IPBX configuration | Contexts   | yes    |
          | IPBX        | IPBX settings      | Users      | yes    |
          | IPBX        | IPBX settings      | Devices    | yes    |
          | IPBX        | IPBX settings      | Lines      | yes    |
          | IPBX        | IPBX settings      | Groups     | yes    |
          | IPBX        | IPBX settings      | Voicemails | yes    |
          | IPBX        | IPBX settings      | Meetme     | yes    |
          | IPBX        | Call Management    | Incall     | yes    |
          | IPBX        | Call Management    | Callfilter | yes    |
          | IPBX        | Call Management    | Pickup     | yes    |
          | IPBX        | Call Management    | Schedule   | yes    |
          | Call Center | Settings           | Queues     | yes    |
          | Call Center | Settings           | Agents     | yes    |

        Given there are contexts with infos:
          | type   | name    | range_start | range_end | entity_name   | didlength |
          | user   | foo     | 1000        | 1999      | entity_filter |           |
          | user   | bar     | 1000        | 1999      | default       |           |
          | group  | foo     | 2000        | 2999      | entity_filter |           |
          | queue  | foo     | 3000        | 3999      | entity_filter |           |
          | meetme | foo     | 4000        | 4999      | entity_filter |           |
          | incall | alberta | 1000        | 4999      | entity_filter | 4         |

        Given the latest plugin "xivo-aastra" is installed

        Given I have the following devices:
          |             ip | mac               | latest plugin of | model | vendor |
          | 192.168.32.101 | 00:00:00:df:ef:01 | xivo-aastra      | 6757i | Aastra |
          | 192.168.32.102 | 00:00:00:df:ef:02 | xivo-aastra      | 6757i | Aastra |
          | 192.168.32.103 | 00:00:00:df:ef:03 | xivo-aastra      | 6757i | Aastra |

        Given there are users with infos:
          | firstname      | lastname | number | context | entity_name   | bsfilter  | device            |
          | _entity_filter | default  |   1101 | default |               |           | 00:00:00:df:ef:01 |
          | _entity_filter | foo      |   1101 | foo     | entity_filter |           | 00:00:00:df:ef:02 |
          | boss           | 1        | 1405   | foo     | entity_filter | boss      |                   |
          | secretary      | 1        | 1410   | foo     | entity_filter | secretary |                   |
          | boss           | 2        | 1406   | default |               | boss      |                   |
          | secretary      | 2        | 1411   | default |               | secretary |                   |

        Given there is a group "groupe" with extension "2222@default"
        Given there is a group "entity_filter" with extension "2555@foo"

        Given I have the following voicemails:
          | name          | number | context |
          | entity_filter |  1234  | foo     |
          | vm003         |  4321  | default |

        Given there are the following conference rooms:
          | name          | number | context |
          | entity_filter |  4234  | foo     |
          | mm001         |  4321  | default |

        Given there are incalls with infos:
          | extension | context     |
          |      4234 | alberta     |
          |      4321 | from-extern |

        Given there is a agent "entity_filter" "" with extension "1111@foo"
        Given there is a agent "agent02" "" with extension "2222@default"

        Given there are queues with infos:
          | name           | display name   | number | context |
          | qentity_filter | qentity_filter | 3000   | foo     |
          | q01            | q01            | 3001   | default |

        Given there is no callfilter "entity_filter"
        Given there is no callfilter "no_filter"
        Given there are callfilters:
         | name          | boss   | secretary   | entity        |
         | entity_filter | boss 1 | secretary 1 | entity_filter |
         | no_filter     | boss 2 | secretary 2 |               |

        Given there is no pickup "entity_filter"
        Given there is no pickup "no_filter"
        Given there are pickups:
          | name          | entity        |
          | entity_filter | entity_filter |
          | no_filter     |               |

        Given there are schedules:
          | name          | entity        |
          | entity_filter | entity_filter |
          | no_filter     |               |

        When I logout from the web interface
        When I login as admin1 with password admin1 in en

        Then I see the context "foo" exists
        Then I see the context "bar" not exists

        When I search for user "_entity_filter" "foo"
        Then user "_entity_filter foo" is displayed in the list
        When I search for user "_entity_filter" "default"
        Then user "_entity_filter default" is not displayed in the list

        Then I see the line "1101" exists
        Then I see the line "1501" not exists

        Then I see the group "entity_filter" exists
        Then I see the group "groupeeeeeeee" not exists

        Then I see the voicemail "entity_filter" exists
        Then I see the voicemail "vm003" not exists

        Then I see the conference room "entity_filter" exists
        Then I see the conference room "mm001" not exists

        Then I see the incall "4234" exists
        Then I see the incall "4321" not exists

        Then agent "entity_filter" is displayed in the list of "default" agent group
        Then agent "agent02" is not displayed in the list of "default" agent group

        Then I see the queue "qentity_filter" exists
        Then I see the queue "q01" not exists

        Then callfilter "entity_filter" is displayed in the list
        Then callfilter "no_filter" is not displayed in the list

        Then pickup "entity_filter" is displayed in the list
        Then pickup "no_filter" is not displayed in the list

        Then schedule "entity_filter" is displayed in the list
        Then schedule "no_filter" is not displayed in the list

        Then there is no device "00:00:00:df:ef:01"

        Then I see devices with infos:
        | mac               | configured |
        | 00:00:00:df:ef:02 | True       |
        | 00:00:00:df:ef:03 | False      |
