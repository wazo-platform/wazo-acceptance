Feature: ProvdPluginUpdate
    In order to update plugins
    I have successfully update

    Scenario: Update plugins in provd
        Given a update plugins provd with good url
        Then plugins list successfully updated
        Given a update plugins provd with bad url
        Then plugins list has a error during update

    Scenario: Aastra switchboard plugin language installation
        Given the plugin "xivo-aastra-switchboard" is not installed
        Given the provisioning plugin cache has been cleared
        Given the plugin list has been updated
        When I install the plugin "xivo-aastra-switchboard"
        When I install the "lang" firmware
        Then the firmware is successfully installed
