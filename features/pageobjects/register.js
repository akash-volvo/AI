const { $ } = require('@wdio/globals');
const Page = require('./page');

class RegisterPage extends Page {
    open() {
        return super.open('register');
    }

    getSuccessMessage() {
        return $('#status').isDisplayed();
    }

    get inputUsername() {
        return $('#username');
    }

    get inputPassword() {
        return $('#password');
    }

    get btnSubmit() {
        return $('button');
    }

    get inputFirstName() {
        return $('#firstName');
    }

    get inputLastName() {
        return $('#lastName');
    }

    get inputEmail() {
        return $('#email');
    }

    get inputPhone() {
        return $('#phone');
    }

    get inputAddress() {
        return $('#address');
    }

    get inputCity() {
        return $('#city');
    }

    get inputState() {
        return $('#state');
    }

    get inputZip() {
        return $('#zip');
    }

    get selectCountry() {
        return $('#country');
    }

    get inputDOB() {
        return $('#dob');
    }

    get radioGenderMale() {
        return $('#male');
    }

    get radioGenderFemale() {
        return $('#female');
    }

    get checkboxInterestSports() {
        return $('#sports');
    }

    get checkboxInterestMovies() {
        return $('#movies');
    }
    
    async register(data) {
        try {
            await browser.pause(1500);
            await this.inputFirstName.setValue(data.firstName);
            await this.inputLastName.setValue(data.lastName);
            await browser.pause(750);
            await this.inputEmail.setValue(data.email);
            await this.inputPhone.setValue(data.phone);
            await browser.pause(750);
            await this.inputAddress.setValue(data.address);
            await this.inputCity.setValue(data.city);
            await this.inputState.setValue(data.state);
            await this.inputZip.setValue(data.zip);
            await browser.pause(750);
            await this.selectCountry.selectByVisibleText(data.country);
            await browser.pause(750);
            await this.inputDOB.setValue(data.dob);
            if (data.gender === 'male') {
                await this.radioGenderMale.click();
            } else if (data.gender === 'female') {
                await this.radioGenderFemale.click();
            }
            if (data.interests.includes('sports')) {
                await this.checkboxInterestSports.click();
            }
            if (data.interests.includes('movies')) {
                await this.checkboxInterestMovies.click();
            }

            await this.inputUsername.setValue(data.username);
            await this.inputPassword.setValue(data.password);

            await browser.pause(1000);

            await this.btnSubmit.click();

        } catch (error) {
            console.error('Error registering user:', error);
            process.exit(1);
        }
    }
}

module.exports = new RegisterPage();
