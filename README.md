Vremenska postaja na mikrokrmilniku Raspberry Pi
======================

Repozitorij vsebuje vse datoteke uporabljene za postavitev vremenske postaje. Postaja je bila narejena kot diplomsko delo. Navodila za postavitev so jasno opisana v javno dostopnem pdfju ki je objavljen na repozitoriju diplomskih del FRI. 


Seznam in opis datotek repozitorija
==================================

* webapp.py - jedro programa, ki  iz baze bere podatke in jih posreduje predlogi Mako,
* refresh.py - program za ustvarjanje seje in za skrb pravilno urejenih podatkov pred vnosom v podatkovno bazo (z pogonom te datoteke lahko ročno vnesemo trenutne meritve),
* index.htm - osnova html strani na podlagi predloge Mako (skrbi za prikaz elementov na spletni strani),
* i2c.py - program za branje iz I\textsuperscript{2}C senzorja (branje temperature in pritiska),
* init_db.py - skrbi za kreiranje podatkovne baze (v kolikor hočemo na novo kreirati podatkovno bazo),
* alchemy_interface.py - vsebuje lastnosti in pravila vnosov v podatkovno bazo,
* measures.db - že obstoječa podatkovna baza (v kolikor želimo novo, jo lahko zbrišemo in na novo kreiramo tako, da poženemo program clr_db.py),
* prod.conf - vsebuje nastavitve za prikazovanje statičnih slik na spletni strani,
* clr_db.py - program za izbris automatski izbris in kreiranje nove podatkovne baze,
* run_script.sh - skripta za posredovanje zagona datoteke za branje iz senzorjev, 
* mapa css - vsebuje Bootstrap datoteke za lepši izgled spletne strani,
* mapa js - nekatere Bootstrap datoteke za poganjanje JavaScript in jQuery knjižnic (nekatere so dostopane preko interneta),
* mapa img - v teji mapi so shranjene vse slike, ki so prikazane na spletni strani,
* mapa eagle - v tej mapi se nahaja shema vseh povezav narejena v programu eagle.