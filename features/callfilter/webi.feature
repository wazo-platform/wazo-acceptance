Feature: Callfilter

    Scenario: Add a callfilter
        Given there is no callfilter "totitatu"
        Given there are users with infos:
         | firstname   | lastname   | number | context | bsfilter  |
         | Sylvain     | Boily      |   1405 | default | boss      |
         | Angelique   | Dedelot    |   1410 | default | secretary |
        When I create a callfilter "totitatu" with a boss "Sylvain Boily" with a secretary "Angelique Dedelot"
        Then callfilter "totitatu" is displayed in the list
