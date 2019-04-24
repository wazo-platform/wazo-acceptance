# Should be in xivo-provd integration tests
Feature: ProvdPluginUpdate

    Scenario: Update plugins in provd
        Given a update plugins provd with good url
        Then plugins list successfully updated
        Given a update plugins provd with bad url
        Then plugins list has a error during update
