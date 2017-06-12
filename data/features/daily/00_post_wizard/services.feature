Feature: wazo-service

  Scenario: Check that wazo-service works properly
    Given the asset file "wazo-service-test.py" is copied on the server into "/tmp"
    Then executing "/tmp/wazo-service-test.py" should complete without errors
