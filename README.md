# Proiect Ingineria Programării

## Membrii echipei:

* Atudore Darius
* Blaga Lucian Florin
* Cernat Alexandru Ionut
* Dumea Alexandru-Gabriel
* Rusu Marius
* Valeanu Cosmin-Teodor

## [Document de analiză a cerințelor clientului](https://docs.google.com/document/d/17vqZvbIErwCdrYLQ1DxoEn_ivvmgSLdzkw3ZzswMQS8/edit?usp=sharing)

---

## [Manual de utilizare](MANUAL.md)

---

## Installation

### Install VLC

Our audio system integrates with the VLC player to allow for media control. You can download it [here](https://www.videolan.org/vlc/).

### Create local Python environment

```cmd
python -m pip install virtualenv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
flask run
```

## For devs

Use ```pip freeze > requirements.txt``` to update the app's dependency list upon adding new packages.

## Run tests

* Linux ```./run_tests.sh```
* Windows ```./run_tests.bat```