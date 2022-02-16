# coding=utf-8

"""
Entspricht den Werten des Online-Rechners von
(1) https://www.sparkasse.de/themen/eigenheim-finanzieren/tilgungsfalle.html
(2) https://www.verivox.de/baufinanzierung/tilgungsrechner/
(3)* https://www.finanztip.de/baufinanzierungsrechner/
(4)* https://tilgungsrechner.fmh.de/rechner3/fmh2/tilgungsrechner/

* kleine Abweichungen von einstelligen Eurobeträgen pro Jahr
"""

__author__      = 'Alf Köhn-Seemann'
__email__       = 'alf.koehn@posteo.net'
__copyright__   = 'Alf Köhn-Seemann'
__license__     = 'MIT'

import time

print( "-------------------------------------------------------------------------------" )
print( "   Tilgungsplan für deinen Kredit" )
print( "-------------------------------------------------------------------------------" )
print( "Kreditsumme = Immobilienpreis - Eigenanteil" )
print( "              + Maklergebühren " )
print( "              + Grunderwerbsteuer (5 % von Immobilienpreis) " )
print( "              + Notargebühr (2 % von Immobilienpreis) " )
print( "Annahme: Annuitätsdarlehen (üblichste Form)" )
print( "         ==> monatliche Zahlung bleibt immer gleich" )
print( "         ==> Zusammensetzung der Zahlung verändert" )
print( "             wird jährlich (?) neu berechnet" )
print( "Annahme: Zahlung beginnt mit nächstem Monat." )
print()
print( "Gib jetzt die Parameter ein, um deinen Tilgungsplan zu berechnen." )

# Abfrage der notwendigen Parameter zur Berechnung
schulden        = float( input("Kreditsumme in Euro        : ") )
zinssatz        = float( input("Zinssatz (Prozent pro Jahr): ") )
tilgung_prozent = float( input("Tilgung (Prozent pro Jahr) : ") )

tilgung_euro    = schulden * tilgung_prozent/100.

# anfänglicher Tilgungssatz, bleibt bei Annuitätsdarlehen konstant
# 1/12 des Betrages wird monatlich abgebucht
zahlung_0       = tilgung_euro + schulden * zinssatz/100.

# aktuelles Jahr und Monat als Startpunkt ermitteln
jahr    = time.localtime()[0]
monat_0 = time.localtime()[1]

print()
print( "-------------------------------------------------------------------------------" )
print( "  Jahr | Schulden | Zahlung | Tilgungsanteil | Zinsanteil | Zinsen aufsummiert " )
print( "-------+----------+------------------------------------------------------------" )

# durch die Monate und Jahre laufen, bis Kredit abgezahlt ist
# Achtung: die Raten werden monatlich aktualisiert
zinsen_summe        = .0            # insgesamt gezahlte Zinsen
zinsen_jahr_sum     = 0             # für laufendes Jahr aufsummierter Zinsanteil
monat               = monat_0 + 1   # Zähler für den aktuellen Monat
tilgung_noZins_sum  = 0             # für laufendes Jahr aufsummierter Tilgungsanteil
zahlung_jahr_sum    = 0             # für laufendes Jahr aufsummierte Zahlungen
while schulden > tilgung_euro:
    zinsen_monat    = schulden * zinssatz/100. / 12.
    zinsen_jahr_sum+= zinsen_monat
    zinsen_summe   += zinsen_monat

    tilgung_noZins_monat    = zahlung_0/12. - zinsen_monat
    tilgung_noZins_sum     += tilgung_noZins_monat

    zahlung_jahr_sum       += zahlung_0/12.

    schulden       -= tilgung_noZins_monat

    monat          += 1

    if monat == 13:
        print( " {0:4d}  |  {1:6d}  |  {2:5d}  |     {3:5d}      |   {4:5d}    |    {5:6d}".format(
            jahr, round(schulden), round(zahlung_jahr_sum), 
            round(tilgung_noZins_sum),
            round(zinsen_jahr_sum), round(zinsen_summe)) )

        # zum Ende des Jahres müssen einige Zähler zurückgesetzt werden
        jahr               += 1
        monat               = 1
        zinsen_jahr_sum     = 0
        zahlung_jahr_sum    = 0
        tilgung_noZins_sum  = 0

print( "-------------------------------------------------------------------------------" )

