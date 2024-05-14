Feature: User Login

  Scenario: Log into the system
    Given I am on the login page
    When I login with <username> and <password>
    Then I should see a flash message that starts with <message>

    Examples: 
      | username | password | message                      |
      | Akash    | pass123  | Welcome to Volvo Cars, Akash |
#      | John     | qwe123   | Welcome to Volvo Cars, John  |
#      | Zack     | 123321   | Welcome to Volvo Cars, Zack  |
