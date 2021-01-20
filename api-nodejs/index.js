const fs = require('fs');

const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
    if (req.query.account === undefined ) {
        res.send('Usage : http://host:port/?account=number');
    }
    else {
        let rawData = fs.readFileSync('./account.json');
        let accountsMock = JSON.parse(rawData);
        var results = {};
        var searchField = "num";
        for (var i=0 ; i < accountsMock.accounts.length ; i++) {
            if (accountsMock.accounts[i][searchField] == req.query.account) {
                results = accountsMock.accounts[i];
            }
        }
        res.send(JSON.stringify(results));
    }
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})