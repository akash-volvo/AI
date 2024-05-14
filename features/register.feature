Feature: User Registration

  Scenario: Register a new user
    Given I am on the registration page
    When I register with "<username>" and "<password>"
    Then I should see a registration success message

    Examples: 
      | username | password |
      | Akash    | pass123  |
#      | John    | qwe123   |
#      | Zack    | 123321 |
