Feature: Backup

  Scenario: Log Rotate Backup Files
    Given there are backup files
    Then backup files successfully rotated

  @no_cleanup_errors_fail
  Scenario: Backup and restore database
    Given the backup manager asset is copied on the server
    When I execute database backup command

    Given there are authentication users with infos:
      | firstname | username | password |
      | Greg      | greg     | 123test  |
    Then I see a user with username "greg"
    When I execute database restore command
    Then the user with username "greg" does not exist
