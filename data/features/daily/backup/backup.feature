Feature: Backup

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
        When I download backup file "test_big_file.tgz"
        Then a non-empty file "test_big_file.tgz" is present on disk

    Scenario: Backup consul data
      Given the asset file "xivo-backup-manager" is copied on the server into "/tmp"
      When I create a consul key "foo" with value "bar"
      When I execute a data backup command
      When I remove the directory "/var/lib/consul"
      When I execute a data restore command
      Then the consul key "foo" equals to "bar"
