Feature: PostInstall Files

    Scenario: Asterisk Voicemail Directory
        Then directory of the Asterisk voicemail is empty

    Scenario: Sound Files Installed
        Then Asterisk sound files correctly installed

    Scenario: Asterisk Owns Dahdi
        Then Asterisk owns /dev/dadhi

    Scenario: Asterisk MOH files Permission
        Then MOH files owned by asterisk:www-data

    Scenario: Log Rotate Backup Files
        Then backup files successfully rotated

    Scenario: Asterisk Max File Descriptors
        Then max open file descriptors are equals to 8192

    Scenario: Debian sources list points on right mirrors
        Then sources.list point on right mirrors
