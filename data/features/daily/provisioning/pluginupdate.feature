Feature: ProvdPluginUpdate
    In order to update plugins
    I have successfully update

    @skip_old_webi_step
    Scenario: Update plugins in provd
        Given a update plugins provd with good url
        Then plugins list successfully updated
        Then directory of the dhcpd update not empty
        Given a update plugins provd with bad url
        Then plugins list has a error during update

    @skip_old_webi_step
    Scenario: Aastra plugin language installation
        Given there's no plugins "xivo-aastra" installed
        Given the provisioning plugin cache has been cleared
        Given the plugin list has been updated
        When I install the latest plugin "xivo-aastra"
        When I install the "lang" firmware for the latest plugin "xivo-aastra"
        Then the firmware is successfully installed
