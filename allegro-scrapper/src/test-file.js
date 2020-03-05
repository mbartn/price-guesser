const rp = require('request-promise');
const fs = require('fs');
const cheerio = require('cheerio')

// doSth();
prepareData();

async function doSth() {
    scrappingUrl = 'https://allegro.pl/oferta/wazon-kufel-krakowski-instytut-szkla-sluczan-ork-9023435870';

    var res = await rp(scrappingUrl);
    console.log(res);
}


async function prepareData() {
    var html = fs.readFileSync('./result.html', 'utf-8');
    const $ = cheerio.load(html);
    $('article').each(function (i, elem) {
        const articleHtml = cheerio.load($(this).html());
        console.log('tytuł:' + articleHtml('h2').text());
        console.log('cena: ' + articleHtml('._9c44d_1zemI').text());
        console.log('cena z dostawa: ' + articleHtml('._9c44d_21XN-').text());
        console.log('stan: ' + articleHtml('._9c44d_wFSmn dl dd').text());
        console.log('nr aukcji: ' + $(this).attr('data-analytics-view-value'));
        // mozna wejsc po linku https://allegro.pl/oferta/${nr_aukcji}

        console.log('\n')
    });


}