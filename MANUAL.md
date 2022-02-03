# Manual de utilizare

## Instalare

### Instalarea VLC

Sistemul nostru audio se integreaza cu player-ul VLC pentru a permite controlul media. Descărcați VLC de [aici](https://www.videolan.org/vlc/).

### Crearea environment-ului local Python

```cmd
python -m pip install virtualenv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### :warning: Dependency hotfix

YouTube a ascuns numărul de dislike-uri, cauzând una din librăriile folosite sa eșueze la rulare. Până când dezvoltatorul va rezolva problema, trebuie sa executăm următorii pași:

* Navigați către folderul ```venv/Lib/site-packages/```
* Localizați folderul ```pafy```
* Deschideți fișierul ```pafy/backend_youtube_dlp.py```
* Modificați linia 54 astfel: ```self._dislikes = 0```
* Salvați fișierul

### Rularea aplicației

```flask run```

### Rularea testelor

* Linux ```./run_tests.sh```
* Windows ```./run_tests.bat```

## Utilizare

Aplicația se poate utliza folosind Postman/Insonia sau direct prin documentația Swagger de la link-ul localhost:5000/swagger.

Pentru început, este nevoie de configurarea a cel puțin un minihub. După crearea minihub-urilor este nevoie de un restart al aplicației pentru a le permite minihub-urilor să ruleze pe port-uri individuale.

După restart, se pot crea și configura utilizatori care se pot mută dintr-o camera în altă (de la un minihub la altul), pot schimbă query-ul folosit pentru media playback, și pot controla minihub-ul din camera în care se află (play, pause, volume up/down).

Deoarece aplicația noastră folosește multithreading putem avea numeroși utilizatori care ascultă muzică în același timp(atât timp cât fiecare este conectat la un minihub diferit).
