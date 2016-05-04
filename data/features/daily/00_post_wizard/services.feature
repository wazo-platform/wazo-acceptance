Feature: xivo-service

  Scenario: Check that xivo-service works properly
    Given the asset file "xivo-service-test.py" is copied on the server into "/tmp"
    Then executing "/tmp/xivo-service-test.py" should complete without errors
