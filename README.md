### Soveltava matematiikka ja fysiikka ohjelmoinnissa

## Fysiikan lopputyö

Projektina suoritetaan samanaikaisesti mitattujen GPS- ja kiihtyvyyshavaintojen analyysi ja tuotetaan siitä laadukas visualisointi.  Työn tuloksena syntyy eräänlainen urheilusovelluksen prototyyppi, jonka avulla voi esimerkiksi analysoida mitattua liikettä harjoittelun ajalta. 

# Mittaukset

Kävele ulkona vähintään muutaman minuutin ajan ja mittaa samalla kiihtyvyyttä ja sijaintia Phyphox-sovelluksella. Pidä puhelin koko ajan samassa asennossa, mielellään melko lähellä ylävartaloa. 

Sinun tulee tässä mitata kahta suuretta samanaikaisesti:

- Valitse Phyhoxista plus-symboli oikeasta alanurkasta
- Valitse "Add simple experiment"
- Valitse sensorit "Linear Acceleration" ja "Location"
- Paina ok, käynnistä mittaus aukeavassa "My experiment" -ikkunassa kun olet valmis aloittamaan mittauksen. 

Mittauksen aikana kannattaa vilkuilla Location-välilehteä. GPS-signaalin löytymisessä kestää aikansa. Voit myös pysyä ensin paikallasi ja lähteä liikkumaan vasta, kun GPS-signaali näyttää löytyneen. Voit sitten myöhemmin poistaa molemmista datoista alkupätkän, jonka aikana et liikkunut. 

Mittaus toimii kuten ennenkin, mutta tuottaa nyt kaksi csv-tiedosto (Accelerometer.csv ja Location.csv).

Jos olet estynyt liikkumaan ulkotilassa, ole yhteydessä opettajaan. 

## Analyysi ja visualisointi

Tutki, missä kiihtyvyyden komponentissa kävelyliike havaitaan parhaiten, valitse se analyysiin kiihtyvyyden osalta.

Määrittele havainnoista kurssilla oppimasi perusteella seuraavat asiat ja esitä ne numeroina visualisoinnissasi:

- Askelmäärä laskettuna suodatetusta kiihtyvyysdatasta

- Askelmäärä laskettuna kiihtyvyysdatasta Fourier-analyysin perusteella

- Keskinopeus (GPS-datasta)

- Kuljettu matka (GPS-datasta)

- Askelpituus (lasketun askelmäärän ja matkan perusteella)

Esitä seuraavat kuvaajat

- Suodatettu kiihtyvyysdata, jota käytit askelmäärän määrittelemiseen. 

- Analyysiin valitun kiihtyvyysdatan komponentin tehospektritiheys

- Reittisi kartalla
