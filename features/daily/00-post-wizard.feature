Feature: Wazo system global checks

  Scenario: Check that the wazo server has a uuid
    Then server has uuid

  Scenario: Check that wazo-service works properly
    Given the asset file "wazo-service-test.py" is copied on the server into "/tmp"
    Then executing "/tmp/wazo-service-test.py" should complete without errors
