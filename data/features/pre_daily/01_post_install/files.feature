Feature: PostInstall Files

    Scenario: Debian sources list points on right mirrors
        Then the mirror list contains a line matching "mirror.wazo.community"
