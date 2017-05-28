'''
This is a code fragment used to add examples for Russian Wiktionary.
(c) Fyodor Sizov, 2017
'''

import buildDictionaryFormat

e = buildDictionaryFormat.examples()
e.add_example('https://ru.wiktionary.org/wiki/%D0%BB%D0%BE%D1%81%D1%8C', 'лось',
    {
        '[ɫosʲ]' : 'mark.ipa',
        '[ɫosʲɪ]' : 'mark.ipa',
        'жвачное парнокопытное млекопитающее с широкими лопатообразными рогами у самцов, самый крупный вид семейства оленей' : 'meaning',
        'перен.' : 'mark.sem',
        'пренебр.' : 'mark.sem',
        'крупный, но неповоротливый человек' : 'meaning',
        'Из всех зверей, обитающих в наших русских лесах, самый крупный и самый сильный зверь ― лось' : 'cite.body',
        'И. С. Соколов-Микитов' : 'cite.author',
        '«Лоси»' : 'cite.name',
        '1923–1928 г.' : 'cite.year',
        'сохатый' : 'link*syn',
        'медведь' : 'link*syn',
        'увалень' : 'link*syn'
    }
)
e.add_example(
    'https://ru.wiktionary.org/wiki/%D1%83%D0%B7%D0%BE%D1%80%D0%B8%D1%81%D1%82%D0%BE',
    'узористо',
    {
        '[ʊˈzorʲɪstə]' : 'mark.ipa',
        'рег.' : 'mark.sem',
        'наречие к прилагательному узористый' : 'meaning',
        'с узорами' : 'meaning'
    }
)