Feature: Backup

    Scenario: Log Rotate Backup Files
        Then backup files successfully rotated

    Scenario: Backup and restore database
        Given the asset file "xivo-backup-manager" is copied on the server into "/tmp"
        Given there is no user "Greg" "Backup"
        When I execute database backup command

        Given there are users with infos:
            | firstname | lastname |
            | Greg      | Backup   |
        Then I see a user with infos:
            | fullname    |
            | Greg Backup |

        When I execute database restore command
        Then the user "Greg" "Backup" not exist

    Scenario: Create backup file
        Given there is a backup file "test_big_file.tgz"
        Given there is no downloaded file "test_big_file.tgz"
        When I download backup file "test_big_file.tgz"
        Then a non-empty file "test_big_file.tgz" is present on disk
