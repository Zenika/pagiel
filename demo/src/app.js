const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.use(express.static('src/public'));

app.get('/api/meaning', (req, res) => {
    setTimeout(() => {
        res.set('Content-Type', 'text/html');
        res.send({message: '42 !!'});
    }, 2000);
});

app.listen(port, () => {
    console.log('Server app listening on port ' + port);
});