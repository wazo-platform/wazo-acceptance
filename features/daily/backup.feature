Feature: Backup

    Scenario: Log Rotate Backup Files
        Given there are backup files
        Then backup files successfully rotated

    Scenario: Backup and restore database
        Given the asset file "xivo-backup-manager" is copied on the server into "/tmp"
        And there is no user "Greg" "Backup"
        When I execute database backup command

        Given there are users with infos:
            | firstname | lastname |
            | Greg      | Backup   |
        Then I see a user with infos:
            | fullname    |
            | Greg Backup |

        When I execute database restore command
        Then the user "Greg" "Backup" not exist
