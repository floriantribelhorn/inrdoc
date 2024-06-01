In diesem Verzeichnis arbeiten wir an einer Applikation, mit welcher Patienten/Patientinnen zu Hause selbstständig Ihre Quick-Messungen (INR) verwalten können.

Funktionen: 
- Profil erstellen
  (username (unique), Vorname, Nachname, Geburtsdatum, Passwort, angewendetes Medikament, Messgerät und LOT-Dokumentation, INR-Zielwerte)
- Einloggen
  (username und dazugehöriges Passwort abfragen und automatisch weiterleiten)
- INR-Messwerte eintragen und abspeichern
  (incl. errechneter Quick und Sekunden anhand der LOT-Daten des jeweiligen Testreagenz)
- INR-Messwerte als Graphen (plotly Library) ausgeben
  (Auswahlmöglichkeit ziwschen verschiedenen Zeithorizonten)
- INR-Daten verwalten
  (Löschfunktion)
- Ausloggen
  (alles session_states zurücksetzen und auf Hauptseite umleiten)

Ausblick:
- Datenwissenschaft: evtl. Admin/Superuser Profil, um alle Daten aller Patienten zu vergleichen
- verschiedene Medikamente/Dosen für jeweilige Patienten
- Dosis/Medikamentenmanagement
- Mail Link mit behandelndem Arzt
- Reminder für Messeingabe (evt. Whatsapp/E-Mail/SMS)
- Daten Editieren -> Checkboxen beim Anwählen so codieren, dass nicht immer lädt
