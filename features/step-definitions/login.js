const { Given, When, Then } = require('@cucumber/cucumber');
const LoginPage = require('../pageobjects/login');
const HomePage = require('../pageobjects/home');

Given(/^I am on the login page$/, async () => {
    await LoginPage.open();
});

When(/^I login with (\w+) and (.+)$/, async (username, password) => {
    await LoginPage.login(username, password);
});

Then(/^I should see a flash message that starts with (.+)$/, async (message) => {
    await HomePage.open();
    await expect(HomePage.welcomeMessage).toBeExisting();
    await expect(HomePage.welcomeMessage).toHaveTextContaining(message);
});