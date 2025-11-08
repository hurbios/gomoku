# Viikkoraportti - Viikko 2
Tällä viikolla muutin hiukan koodin rakennetta ja paransin luettavuutta. Tämän viikon tavoitteena oli lisäillä testit ja testikattavuus. Lisäsin pytestin testausta varten ja tein ensimmäiset testit. Tämän jälkeen lisäsin testauksen myös automaattiseen Github Actions workflowhun. Näin ei unohdu pitää testejä ajan tasalla ja myöskin tulee heti huomattua mikäli jokin muutos rikkoo olemassa olevaa toiminnallisuutta. Kun olin tehnyt testejä riittävästi lisäsin coveragen projektiin. Tämä auttoi huomaamaan mitkä osiot oli vielä testaamatta. Lisäsin testejä ja tällä löytyikin pieniä bugeja jotka samalla myös korjasin. Jätin UIn testien ulkopuolelle kurssin ohjeistuksen mukaisesti ja lisäsin coveragen configuraation joka oli linjassa tämän kanssa. Lopuksi vielä lisäsin coveragen raportin projektin readmeen. [![codecov](https://codecov.io/github/hurbios/gomoku/graph/badge.svg?token=TGI5QXQLXL)](https://codecov.io/github/hurbios/gomoku)

Seuraavaksi aloitin algoritmin hahmottelun. Huomasin algoritmia tehdessä että game_board kaipasi lisää toiminnallisuuksia. Tässä vaiheessa on ajatuksena että game_board toimisi pohjana pelitilanteen tiedoista ja siksi tuota käytetäänkin algoritmin kanssa. Tämä muutetaan mahdollisesti myöhemmin välimuistin lisäyksen yhteydessä siten että game_board pitää kirjaa vain oikeasta pelitilanteesta. Tosin tätä muokatessa olisi varmaankin hyvä miettiä että mikä on tehokkain tapa pitää kirjaa niin ettei tule kirjattua samaa asiaa useaan kertaan.

Algoritmi toimii näin aluksi vain blokkaamalla. Tämä toimiikin jo yllättävän hyvin ollakseen ihan alkutekijöissä. Algoritmin kehitys tapahtui pitkälti yksikkötestien avulla. Kun olin saanut algoritmin siihen tilaan että se vaikutti toimivan suhteellisen hyvin blokkaamaan tehtyjä siirtoja, päätin lisätä sen peliin. Nyt peliä voi pelata tuon kanssa. AI blokkaa tehokkaasti siirtoja mutta se on pienellä strategialla kuitenkin helppo voittaa. Tämän jälkeen tein vielä pieniä parannuksia.

Algoritmin olemassa olevaa toiminnallisuutta voi todennäköisesti käyttää hyödyksi pelitilanteen arvioinnista. Tehty algoritmi ei siis toimi logiikaltaan samalla tavalla kuin lopullinen versio, mutta hyödyttää vähintäänkin oppimisen kautta ja osin voi myös käyttää koodia hyödyksi lopullisessa versiossa. Tässä vaiheessa aloin miettiä tarkemmin miten lopullinen algoritmi tulisi toimimaan ja miten pelitilanteen arvointi menisi. Tämä onkin sitten seuraavan viikon aiheita. Opin tätä heuristiikkaa hahmotellessani miten tuota olisi hyvä tehdä tällaisen pelin yhteydessä. En ollut aiemmin tehnyt mitään tekoälylogiikkaa peleille joten opin jonkin verran siitä mitä se vaatii. Alla on hahmotelmaa millä tavoin yksittäisen siirron hyvyyttä voi pisteyttää. Ensiviikolla on tarkoitus tarkentaa, toteuttaa ja testata näitä pelitilanteiden arviointeja. Tällä viikolla on mennyt projektiin aikaa noin 11 tuntia.



## Draft heuristics for move evaluation
### Move priority:
1.  ATTACK - add 5th for the row
2.  BLOCK - block 5th in a row with one sided empty space
3.  ATTACK - add 4th in a row (one or more empty space)
4.  BLOCK - block 4th in a row with both sides empty space
5.  ATTACK - add center for dual 3rd in a row with empty spaces around (4)
6.  BLOCK - block center for dual 3rd in a row with empty spaces around (4)
7.  ATTACK - add 3rd in a row with empty spaces around (*)
8.  BLOCK - block center for dual 3rd in a row with 3 or less empty spaces around (*)
9.  ATTACK - add 3rd in a row with one side empty space (*)
10. BLOCK - block 4th in a row with one side empty space
11. BLOCK - block 3rd in a row with empty spaces around (*)
12. ATTACK - add 2nd in a row with empty spaces around
13. BLOCK - block 3rd in a row with one side empty spaces around
14. BLOCK - block 2nd in a row with empty spaces around (4)
15. ATTACK - add 1st in a row with as many empty spaces around as possible
* remember that for 4 in a row requires 1 space for either side 
and 3 in a row requires at least 1 space in both sides or 2 spaces in one side. 
With 3 in wor 2+ empty both sides is better than 1+ both sides etc.

### How good a move is
- based on points of the above (probably reversed points)
- check the best what is the best points for the estimated move
    - BLOCK     = minus points
    - ATTACK    = plus points



