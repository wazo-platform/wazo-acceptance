Feature: Parking extensions

    @skip_old_webi_step
    Scenario: Change parking settings
        When I change the parking configuration to be:
        | Extension | Wait delay | Parkings hints | Range start | Range end |
        | 701       | 30 seconds | enabled        | 702         | 750       |
        Then asterisk should have the following parking configuration:
        | Parking Extension | Parking Spaces | Parking Time | Enabled |
        |               701 |        702-750 | 30 sec       | yes     |
