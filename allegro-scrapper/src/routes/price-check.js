var express = require('express');
var router = express.Router();

let ScrapperService = require('../service/scrapper-service');


router.get('/', async function (req, res, next) {

    var response = await ScrapperService.findNewAuctions();
    console.log('Have reponse');
    console.log(response);
    res.send(response);

});

module.exports = router;
