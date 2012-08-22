Feature: backup

    Test X-65

    Scenario: Create backup file
        Given I am logged in
        Given there is a backup file "test_big_file.tgz"
        When I download backup file "test_big_file.tgz"
        Then a non-empty file "test_big_file.tgz" is present on disk
