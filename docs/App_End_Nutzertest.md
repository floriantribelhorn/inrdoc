# ENDTEST durch neuen User

1. Registration des Users funktioniert
    - Registration des Medikaments (inkl. der Lotnummer)
        - Lotnummer wichtig, da bei Lotnummerwechsel auch der tehrapeutische Bereich des INR wechseln kann
    - Registration des Messgerätes
    - Eingabe des medizinisch relevanten INR-Bereiches kann auch eingegeben werden

2. Auf der Startseite sind alle wichtigen Information über die Gerinnungstörung und deren Messung erhalten. bildet einen guten erseten Überblick


3. Der Aufbau ist klar ersichtlich
    - Aufbau der einzelnen Funktion logisch
        - mit Symbolen auch visuell dargestellt
    - Testperson landet am richtigen (gedachten) Ort


4. Änderungen der eingegebenen Daten jederzeit möglich
    - unter "Login/ Registration" können jederzeit alle Userdaten geändert werden
    - wichtig bei Änderung des Medikaments oder des einschränkenden Zielbereiches für die Therapie
    

5. Das App als Quick-Notizbuch gebraucht werden
    - INR-Werte können unter " Messungen" eingegeben werden, mittels drücken der Enter-Taste, werden diese dann automatisch in Prozent des Quicks umgerechnet
        - vereinfacht die Eingabe und vermindert Fehler 
    - im Bereich "Überblick", können die Daten als Graph angeschaut werden
        - tolles Tool, da auch hineingezoomt werden kann oder der Bereich vergrössert werden kann
        - Auch die Jahre sowie die einzelnen Monate sind darin ersichtlich
    - Datenverlauf kann als *.png abgespeichert werden und bei Bedarf versendet werden
    - Alle Daten können im "Editor" angepasst und somit geändert werden, wichtig bei Fehleingabe
    


# Bewertung
Testuser konnte sich ohne Probleme registrieren. Messwerte konnten ohne Probleme eingegeben werden und anschliessend im Bereich "Überblick" angeschaut werden. Der Quick Range wird ausgerechnet indem nur der INR (relevantere Wert) eingegeben werden muss. Die Werte können anschliessend als Grafik auch lokal gespeichert werden um somit ein Dokument für einen allfälligen Besuch bei Hausartz zu haben.
Alles in allem sehr überischtliche (Mit der sidebar-Navigation ist klar ersichtlich bei welcher Seite, welche Funktionen enthalten sind. Auch beim Öffnen der App steht klar geschrieben (2 Buttons Einloggen/Registrieren), wie es weitergehen soll.) App und einfach in der Handhabung, erfüllt seinen Zweck als "Quicktagebuch".

Verbesserungspotential: Was passiert, wenn ein user sein Passwort vergessen hat? Passwort zurücksetzen nicht möglich -> Ausblick-Thema, falls App weiterverfolgt wird. (ev. mit E-Mail-Adressen arbeiten)

# Ausblick
1. Passwort zurücksetzen? E-Mail-Adresse, Verifikation, dass dazugehörige Person, das Passwort willentlich zurücksetzt
2. Login-System mit Capatcha noch sicherer machen und ggf. md5hash noch mit weiteren Schritten sicherer machen
3. Administrator hinzufügen: Verwaltung aktueller/neuer LOT-Daten, nicht mehr genutzte Profile löschen, Daten für Studienzwecke verwalten
4. Erinnerungsfunktion für Patienten (ev. via E-Mail oder SMS oder ggf. bestehende API?)
5. automatisches E-Mail an behandelnden Arzt für Sprechstunde
6. momentan alles noch fiktive LOT-Daten der jeweiligen Messgeräte -> Hersteller kontaktieren, ob ggf. Daten erhältlich wären, um echte Daten zu generieren.
7. Falls user in einem wichtigen Erfassungsschritt (Aktualisieren der Daten im update.py Skript, sign_up.py Skript oder messeingabe.py Skript die Verbindung abgerissen wird, was wird in die DB eingetragen, was nicht? Hat es Einfluss auf den flow in der Applikation? Das müsste alles im Detail noch geprüft werden, weil ansonsten die Gefahr besteht, dass Messwerte mit falschen LOT-Daten eingetragen werden
8. Code z.T. sehr redundant -> nützliche Klassen erstellen, damit nicht immer wieder Code kopiert werden muss

