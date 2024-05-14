const { browser } = require('@wdio/globals');

module.exports = class Page {
    open(pageName) {
        const baseUrl = 'http://localhost:3000';
        return browser.url(`${baseUrl}/${pageName}`);
    }
}
