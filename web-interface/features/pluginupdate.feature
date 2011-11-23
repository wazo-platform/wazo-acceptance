Feature: ProvdPluginUpdate
    In order to update plugins
    I have successfully update

    Scenario Outline: Update plugins in provd
        Given I login as root with password superpass at http://skaro-daily.lan-quebec.avencall.com
        Given a update plugins provd with good url
        Then plugins list successfully updated
        Given a update plugins provd with bad url
        Then plugins list has a error during update
