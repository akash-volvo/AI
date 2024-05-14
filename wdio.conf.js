exports.config = {
    runner: 'local',
    specs: ['./features/register.feature'],
    exclude: [],
    maxInstances: 10,
    capabilities: [{
        browserName: 'chrome',
    }],
    logLevel: 'info',
    waitforTimeout: 60000,
    connectionRetryTimeout: 120000,
    connectionRetryCount: 3,
    framework: 'cucumber',
    reporters: ['spec'],
    cucumberOpts: {
        timeout: 60000,
        require: ['./features/step-definitions/register.js'],
        ignoreUndefinedDefinitions: false
    },
    onComplete: function(exitCode, config, capabilities, results) {
        if (results.failed === 0) {
            console.log("Executing the second feature file...");
            const secondFeatureFilePath = './features/login.feature';
            const wdio = require('@wdio/cli');
            wdio.run({
                specs: [secondFeatureFilePath],
                ...config
            }).then((code) => {
                console.log('Execution of the second feature file completed.');
            }).catch((error) => {
                console.error('Error occurred while executing the second feature file:', error);
            });
        } else {
            console.log('Skipping execution of the second feature file due to failures in the first one.');
        }
    }
};
