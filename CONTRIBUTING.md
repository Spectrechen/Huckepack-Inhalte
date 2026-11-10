# Ein Paket beitragen

## Regeln
- **Eigene Aufgaben.** Keine Aufgaben aus Schulbüchern, Arbeitsheften oder Webseiten abschreiben (Urheberrecht).
  Mit dem Pull Request bestätigst du, dass die Aufgaben von dir sind und unter CC BY 4.0 stehen dürfen.
- **Richtig.** Jede Antwort ist geprüft; Fakten stimmen; Sprache passt für 8–9-Jährige (kurze Sätze, freundlich).
- **Koop.** Jede Aufgabe braucht beide Kinder: Hinweis/Antwort getrennt (`splitInfo`), zwei Rechenschritte (`relay`),
  Paare mit geteilten Hälften (`matchPairs`) oder eine gemeinsame Entscheidung (`bothAgree`).
- **Nichts Persönliches.** Keine echten Namen von Kindern, keine Marken, keine Links, keine Emojis.
- Deutsch (`de`) ist Pflicht, Englisch (`en`) erwünscht.

## Format
Ein Ordner `packs/<paket-id>/` mit `pack.json`. Die Paket-ID hat mindestens drei Teile aus Kleinbuchstaben,
Ziffern und Bindestrichen (`de.dein-name.thema`). Level-IDs beginnen mit `<paket-id>/`. Jedes Level nennt mit
`place` einen Ort der Karte, an dem es als weiterer „Band“ erscheint (z. B. `numbers-hill`, `mill`, `market`,
`clock-tower`, `syllable-school`, `library`, `post-office`, `farm`, `weather-station`, `crossing`, `bus-stop`,
`tea-house`, `zoo`, `lighthouse`). Höchstens 20 Level und 512 KB pro Paket. Das Beispielpaket zeigt alle vier
Aufgabentypen; die genauen Regeln stehen in `CoopTask.swift` der App.

Neue Fähigkeiten (`skills`) bekommen im Paket einen Namen für die Eltern-Auswertung.

## Prüfen
```
git clone https://github.com/Spectrechen/Huckepack
cd Huckepack/Packages/HuckepackCore
swift run huckepack-lint ../../../Huckepack-Inhalte/packs/*/pack.json
```
Eine neue Version eines Pakets erhöht `version`.
