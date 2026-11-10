# Ein Paket beitragen

*English: contribute level packs (extra levels for the Huckepack map) or world packs (own map, places and courses, any
age). Rules: your own tasks, correct, truly co-op, nothing personal, CC BY 4.0. Format: see `docs/FORMAT.md`.*

Beiträge sind willkommen, für die Huckepack-Karte genauso wie für ganz eigene Welten (jedes Alter, Klasse 1 bis 13).
Die Details stehen in der Dokumentation:

- [docs/FORMAT.md](docs/FORMAT.md): vollständige Referenz und Checkliste
- [docs/WELT-ANLEGEN.md](docs/WELT-ANLEGEN.md): Anleitung für eine eigene Welt
- [docs/schema/pack.schema.json](docs/schema/pack.schema.json): JSON Schema für den Editor

## Regeln
- **Eigene Aufgaben.** Keine Aufgaben aus Schulbüchern, Arbeitsheften oder Webseiten abschreiben (Urheberrecht).
  Mit dem Pull Request bestätigst du, dass die Aufgaben (und ein Kartenbild) von dir sind und unter CC BY 4.0 stehen dürfen.
- **Richtig.** Jede Antwort ist geprüft; Fakten stimmen; Sprache passt zum Alter der Kinder (kurze Sätze, freundlich).
- **Koop.** Jede Aufgabe braucht beide Kinder: Hinweis/Antwort getrennt (`splitInfo`), zwei Rechenschritte (`relay`),
  Paare mit geteilten Hälften (`matchPairs`) oder eine gemeinsame Entscheidung (`bothAgree`). Gute und schlechte Beispiele:
  [FORMAT.md, Abschnitt 15](docs/FORMAT.md#15-was-eine-gute-koop-aufgabe-ausmacht).
- **Nichts Persönliches.** Keine echten Namen von Kindern, keine Marken, keine Links, keine Emojis; auch nicht im Kartenbild.
- Deutsch (`de`) ist Pflicht, Englisch (`en`) erwünscht.

## Zwei Arten von Paketen
- **Level-Paket** (ohne `world`): Level für Orte der Huckepack-Karte. Jedes Level nennt mit `place` einen Ort
  (`numbers-hill`, `mill`, `market`, `clock-tower`, `syllable-school`, `library`, `post-office`, `farm`, `weather-station`,
  `crossing`, `bus-stop`, `tea-house`, `zoo`, `lighthouse`) und erscheint dort als weiterer „Band“.
- **Welt-Paket** (mit `world`): eigenes Kartenbild (`.jpg` oder `.png`, höchstens 8 MB, 512 bis 8192 Pixel je Seite), Orte,
  Wege, eigene Kurse (`courses`) und Level. Das Beispiel: [`packs/de.huckepack.beispielwelt`](packs/de.huckepack.beispielwelt/pack.json).

## Format in Kürze
Ein Ordner `packs/<paket-id>/` mit `pack.json` (und bei Welten dem Kartenbild). Die Paket-ID hat mindestens drei Teile aus
Kleinbuchstaben, Ziffern und Bindestrichen (`de.dein-name.thema`) und ist zugleich der Ordnername. Level-IDs beginnen
mit `<paket-id>/`. Höchstens 40 Level je Paket, `pack.json` höchstens 512 KB. Neue Fähigkeiten (`skills`) bekommen im Paket
einen Namen für die Eltern-Auswertung. Eine neue Version eines Pakets erhöht `version`.

## Prüfen
Beim Pull Request prüft GitHub automatisch das Format (`tools/check_format.py`: gültiges JSON, Paket-ID, Level-IDs,
Orte und Wege, Fächer, Kartenbild, Aufgabentypen, Pflichtfelder, Antworten). Die vollständige Prüfung mit den Regeln der App
(`huckepack-lint`) macht der Betreuer vor dem Zusammenführen. Lokal:

```
python3 tools/check_format.py packs/*/pack.json
```
