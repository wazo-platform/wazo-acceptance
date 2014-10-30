Feature: Parking extensions

Scenario: Change parking settings
    When I change the parking configuration to be:
    | Extension | Wait delay | Parkings hints | Range start | Range end |
    | 701       | 30 seconds | enabled        | 702         | 750       |
    Then I should have to following lines in "features show":
    | Parking extension | Parked call extensions | Parkingtime | Enabled |
    |               701 |                702-750 | 30000 ms    | Yes     |
