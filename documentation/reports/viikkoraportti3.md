# Viikkoraportti - Viikko 3
Tällä viikolla olen dokumentoinut ohjelman toiminnallisuutta. Lisäsin ohjelman ylimalkaisen flown ([implementation dokumenttiin](../implementation.md)). Lisäksi lisäsin samaiseen dokumenttiin hahmotelmaa heuristiikasta. Kyseinen heuristiikka toimii hyvin seuraavan siirron prioriteettina ja tämän avulla voi jo pelata peliä suhteellisen hyvin (peli ajoittain rikki uuden kehityksen takia, mutta commit 99156dd sisältää toimivan version). Opin että tämä ei kuitenkaan käy sellaisenaan minimaxin kanssa, mutta antaa hyvää osviittaa ja voi toimia pohjana minimaxissa käytettävään heuristiikkaan.

Minimaxin kehitys on alkanut. Tässä kohtasin pieniä haasteita seuraavan siirron evaluaation kohdalla kun tuntui ettei logiikka oikein toiminut minimaxin kanssa. Itsessään minimax algoritmi pitäisi olla pääpiirteittäin hyvällä tolalla, mutta vielä jokin estää sitä toimimasta.

Lisäilin myös jonkin verran testejä ja aloin kirjoittaa ([testausdokumenttia](../testing.md)). Testikattavuus on nähtävillä projektin README.md tiedostossa ja pylint on ollut käytössä projektissa melkeinpä alusta asti ja lint huomioitu koko kehityksen ajan.

Tällä viikolla aikaa on mennyt noin 8 tuntia projektiin. Aikatauluhaasteiden takia on hieman kirittävä ensi viikolla tavoitteiden saavuttamiseksi. Projektin ydintoiminnallisuutta tukevat metodit alkavat olla lähellä valmistumista kuitenkin ja niille on yksikkötestejä. Näitä voisi kuitenkin vielä hieman lisätä. Seuraavan viikon tavoitteena on erityisesti saada minimax algoritmi toimimaan jonkinlaisen heuristiikan kanssa.
