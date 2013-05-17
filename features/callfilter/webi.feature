Feature: Callfilter

    Scenario: Add a callfilter
        Given there is no callfilter "totitatu"
        Given there are users with infos:
         | firstname   | lastname   | number | context | bsfilter  |
         | Sylvain     | Boily      |   1405 | default | boss      |
         | Angelique   | Dedelot    |   1410 | default | secretary |
        When I create a callfilter "totitatu" with a boss "Sylvain Boily" with a secretary "Angelique Dedelot"
        Then callfilter "totitatu" is displayed in the list

    Scenario: Deactivating a boss deletes the func key
        Given there is no callfilter "bigboss"
        Given there are users with infos:
         | firstname | lastname | number | context | bsfilter  |
         | Sylvain   | Boily    | 1405   | default | boss      |
         | Angelique | Dedelot  | 1410   | default | secretary |
        Given there is a callfilter "bigboss" with boss "Sylvain Boily" and secretary "Angelique Dedelot"
        Given user "Sylvain" "Boily" has the following function keys:
         | Key | Type                       | Destination                 | Label | Supervision |
         | 1   | Customized                 | 1000                        | 1000  | Disabled    |
         | 2   | Filtering Boss - Secretary | bigboss / Angelique Dedelot | boss  | Disabled    |
         | 3   | Customized                 | 1001                        | 1001  | Disabled    |
        When I deactivate boss secretary filtering for user "Sylvain Boily"
        Then the user "Sylvain Boily" has the following func keys:
          | Key | Type       | Destination | Label | Supervision |
          | 1   | Customized | 1000        | 1000  | Disabled    |
          | 3   | Customized | 1001        | 1001  | Disabled    |
