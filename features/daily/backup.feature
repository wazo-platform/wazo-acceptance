Feature: Backup

    Scenario: Log Rotate Backup Files
        Given there are backup files
        Then backup files successfully rotated

    Scenario: Backup and restore database
        Given the asset file "xivo-backup-manager" is copied on the server into "/tmp"
        When I execute database backup command

        Given there are permanent authentication users with info
            | firstname | username | password |
            | Greg      | greg     | 123test  |
        Then I see a user with username "greg"
        When I execute database restore command
        Then the user with username "greg" does not exist
