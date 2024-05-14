const { Given, When, Then } = require('@cucumber/cucumber');
const RegisterPage = require('../pageobjects/register');

Given(/^I am on the registration page$/, async () => {
    await RegisterPage.open();
});

When('I register with {string} and {string}', async (username, password) => {
    await RegisterPage.register({
        firstName: 'Akash',
        lastName: 'R',
        email: 'akash@abc.xyz',
        phone: '9988776655',
        address: 'Manhattan, NY',
        city: 'New York City',
        state: 'New York',
        zip: '11111',
        country: 'USA',
        dob: '02-07-2001',
        gender: 'male',
        interests: ['sports', 'movies'],
        username: username,
        password: password
    });
});


Given(/^I should see a registration success message$/, async () => {
    const isMessageVisible = await RegisterPage.getSuccessMessage();
    expect(isMessageVisible).toBe(true);
});
