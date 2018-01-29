Feature: REST API

  Background: There's an admin and a regular user
    Given the root domain is "mydomain.org"
      And there's admin "admin" with password "kejh2k3hr24w"
      And there's user "tonda" with password "sdfvu43re2"

  Scenario: Add DNS record as admin
    Given we're logged in as "admin" with password "kejh2k3hr24w"
     When we add IP "1.2.3.4" as "home.mydomain.org"
     Then status code is 201
      And there's 1 record for IP "1.2.3.4" and name "home.mydomain.org"
