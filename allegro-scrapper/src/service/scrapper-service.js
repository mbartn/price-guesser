const rp = require('request-promise');
const cheerio = require('cheerio')

class ScrapperService {
    static scrappingUrl = 'https://allegro.pl/kategoria/antyki-26014?order=n';

    constructor() {
    }


    static async findNewAuctions() {

        try {
            var res = await rp(this.scrappingUrl);
            console.log(res);
            console.log($('article', html).length);
            return res;

        } catch (e) {
            console.log('error');
        }

    }
}


module.exports = ScrapperService;

