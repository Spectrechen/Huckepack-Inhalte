# Huckepack-Inhalte

*English: community content for Huckepack, a co-op learning game where two kids play together on two devices. There are two kinds of packs: **level packs** add levels ("Band 2") to places of the Huckepack map; **world packs** bring their own map image, places, paths and courses, for any age (grade 1 to 13). Every task needs both kids. Packs are plain JSON, licensed CC BY 4.0. The app itself is not public yet. Documentation is in German.*

Huckepack ist ein Lernspiel für **zwei Kinder auf zwei Geräten**. Die beiden Figuren laufen gemeinsam über eine Karte,
und jede Aufgabe braucht beide Kinder: Eines sieht den Hinweis, das andere tippt die Antwort; oder sie rechnen eine
Staffel; oder jedes hält die Hälfte der Karten; oder sie müssen sich auf eine Antwort einigen. Keines schafft es allein.
Das ist der Kern des Spiels: miteinander reden, erklären, zuhören.

Dieses Repository sammelt **Inhalte** für Huckepack. Jeder kann welche beitragen, jede Familie kann eigene bauen. Die App
selbst ist noch nicht öffentlich; das Format hier ist aber festgelegt und dokumentiert.

## Zwei Arten von Paketen

| | Level-Paket | Welt-Paket |
|---|---|---|
| Was es ist | Weitere Level („Band 2“, „Band 3“ …) für Orte der Huckepack-Karte | Eine eigene Welt: Kartenbild, Orte, Wege, Kurse und Level |
| Für wen | Alle, die die Huckepack-Welt erweitern wollen (Grundschule, Klasse 3, NRW) | Jede Familie, jedes Alter (Klasse 1 bis 13), z. B. „Kurs A, B, C“ für die eigenen Kinder |
| Dateien | `pack.json` | `pack.json` und das Kartenbild (`karte.jpg`) |
| Anleitung | [docs/FORMAT.md](docs/FORMAT.md) | [docs/WELT-ANLEGEN.md](docs/WELT-ANLEGEN.md) |

## Für Eltern: ein Paket installieren
1. Lade den Ordner eines Pakets aus `packs/` auf das **Eltern-Gerät** (z. B. in „Dateien“). Bei einem Level-Paket genügt die
   Datei `pack.json`; bei einem Welt-Paket braucht ihr den ganzen Ordner mit `pack.json` und dem Kartenbild.
2. In Huckepack auf dem Eltern-Gerät: **Eltern-Bereich › Fächer › „Paket hinzufügen …“**. Bei einem Welt-Paket wählt ihr den Ordner
   des Pakets (mit `pack.json` und Kartenbild). **Schaltet das Paket ein.**
3. Sobald die Geräte der Kinder sich mit dem Eltern-Gerät verbinden, bekommen sie das Paket.
   Beide Kinder brauchen dieselben Pakete.
4. Bei einem Welt-Paket wählen die Kinder die Welt **gemeinsam auf ihrem Startbildschirm** aus.

Huckepack lädt nichts selbst aus dem Internet; die Kinder-Geräte bekommen Pakete nur vom Eltern-Gerät, geprüft über
die signierten Eltern-Einstellungen.

## Pakete
| Paket | Art | Inhalt | Fach |
|---|---|---|---|
| [`de.huckepack.kopfrechnen`](packs/de.huckepack.kopfrechnen/pack.json) | Level-Paket | Kopfrechnen im Zahlenraum 1000 (Beispiel) | Mathe |
| [`de.huckepack.beispielwelt`](packs/de.huckepack.beispielwelt/pack.json) | Welt-Paket | Beispielwelt mit sechs Orten und drei Kursen für 9-Jährige (Vorlage für eigene Welten) | Kurs A: Rechnen, Kurs B: Lesen, Kurs C: Natur |

## Dokumentation
- [docs/FORMAT.md](docs/FORMAT.md): die vollständige Referenz aller Felder, Aufgabentypen, Antwortformate, Grenzen und eine Checkliste.
- [docs/WELT-ANLEGEN.md](docs/WELT-ANLEGEN.md): Schritt für Schritt zur eigenen Welt (Karte malen, Koordinaten, Kurse, Level, prüfen, installieren).
- [docs/schema/pack.schema.json](docs/schema/pack.schema.json): JSON Schema für Editoren (`"$schema": "../../docs/schema/pack.schema.json"` in der `pack.json`).
- [tools/check_format.py](tools/check_format.py): Formatprüfung ohne App (`python3 tools/check_format.py packs/*/pack.json`).

## Mitmachen
Siehe [CONTRIBUTING.md](CONTRIBUTING.md). Jeder Pull Request wird automatisch auf das Format geprüft; danach prüft
der Betreuer ihn mit dem Prüfwerkzeug der App (`huckepack-lint`) und liest ihn fachlich.

## Lizenz
Inhalte: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.de), Rechtstext in [LICENSE](LICENSE), Erläuterung in [LICENSE.md](LICENSE.md).
