const { $ } = require('@wdio/globals');
const Page = require('./page');

class HomePage extends Page {

    get welcomeMessage () {
        return $('#welcome');
    }
    
    open () {
        return super.open('home');
    }
}

module.exports = new HomePage();
