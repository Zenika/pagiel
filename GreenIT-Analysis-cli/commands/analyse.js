const fs = require('fs');
const YAML = require('yaml');
const path = require('path');
const puppeteer = require('puppeteer');
const createJsonReports = require('../cli-core/analyis.js').createJsonReports;
const login = require('../cli-core/analyis.js').login;
const create_global_report = require('../cli-core/report.js').create_global_report;
const create_XLSX_report = require('../cli-core/report.js').create_XLSX_report;
const writeToInflux = require('../cli-core/influxdb.js').write;

//launch core
async function analyse_core(options) {
    const URL_YAML_FILE = path.resolve(options.yaml_input_file);
    //Get list of url
    let urlTable;
    try {
        urlTable = YAML.parse(fs.readFileSync(URL_YAML_FILE).toString());
    } catch (error) {
        throw ` yaml_input_file : "${URL_YAML_FILE}" is not a valid YAML file.`
    }

    //start browser
    const browser = await puppeteer.launch({
        headless:true,
        args :[
            "--no-sandbox",                 // can't run inside docker without
            "--disable-setuid-sandbox"      // but security issues
        ],
        // Keep gpu horsepower in headless
        ignoreDefaultArgs:[
            '--disable-gpu'
        ]
    });
    //handle analyse
    let reports;
    try {
        //handle login
        if (options.login){
            const LOGIN_YAML_FILE = path.resolve(options.login);
            let loginInfos;
            try {
                loginInfos = YAML.parse(fs.readFileSync(LOGIN_YAML_FILE).toString());
            } catch (error) {
                throw ` --login : "${LOGIN_YAML_FILE}" is not a valid YAML file.`
            }
            console.log(loginInfos)
            await login(browser, loginInfos)
        }
        //analyse
        reports = await createJsonReports(browser, urlTable, options);
    } finally {
        //close browser
        let pages = await browser.pages();
        await Promise.all(pages.map(page =>page.close()));
        await browser.close()
    }
    //create report
    let reportObj = await create_global_report(reports, options);
    await create_XLSX_report(reportObj, options)
    if(options.influxdb) {
        await writeToInflux(reports, options)
    }
}

//export method that handle error
function analyse(options) {
    analyse_core(options).catch(e=>console.error("ERROR : \n" + e))
}

module.exports = analyse;