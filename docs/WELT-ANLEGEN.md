# Eine eigene Welt anlegen

*English summary: step-by-step guide for a family that wants its own Huckepack world: paint or photograph a map, read the
coordinates of the places, define courses for your kids, write co-op levels, check the pack and install it on the parent
device. The running example is `packs/de.huckepack.beispielwelt`. The rest is in German.*

Eine eigene Welt ist ein Ordner mit zwei Dateien: einem Kartenbild und einer `pack.json`. Du brauchst dafür keine
Programmierkenntnisse, nur einen Texteditor (am besten Visual Studio Code) und etwas, womit man ein Bild malen oder
bearbeiten kann. Alle Feldnamen erklärt [FORMAT.md](FORMAT.md); hier gehen wir den Weg Schritt für Schritt, und als
Beispiel dient die Beispielwelt in [`packs/de.huckepack.beispielwelt`](../packs/de.huckepack.beispielwelt/pack.json).

Die Grundidee: Huckepack spielen immer **zwei Kinder auf zwei Geräten**. Jede Aufgabe braucht beide: Ein Kind sieht
den Hinweis, das andere tippt die Antwort; oder sie rechnen eine Staffel; oder jedes hält die Hälfte der Karten. Mehr
dazu in [FORMAT.md, Abschnitt 1 und 15](FORMAT.md#1-die-grundidee-zwei-kinder-zwei-geräte). Eure Welt ist dazu der Rahmen:
eine Landkarte, über die die beiden Figuren gemeinsam gehen.

## Schritt 1: Plane die Welt

Überlege zuerst auf Papier:
1. **Wer spielt?** Alter und Klassenstufe der Kinder (das Feld `grade`, 1 bis 13).
2. **Welche Kurse?** In der Beispielwelt für 9-Jährige: *Kurs A: Rechnen*, *Kurs B: Lesen*, *Kurs C: Natur*. Das kann alles
   sein, was ihr üben wollt: Kurse aus der Schule, Englisch-Vokabeln, Dinosaurier.
3. **Welche Orte?** Ein Ort pro Level, dazu ein paar Orte ohne Lernstoff (ein Startlager) und vielleicht ein Spiel
   zwischendurch. Die Beispielwelt hat sechs Orte:

| Ort (`id`) | Name | Was dort ist |
|---|---|---|
| `lager` | Lager | Start, kein Level |
| `baum` | Baumhaus | Level „Kurs A: Rechnen“, dazu ein zweites Level (Band) |
| `see` | See | Level „Kurs C: Natur“ |
| `berg` | Berg | Level „Kurs B: Lesen“, öffnet sich nach dem Baumhaus |
| `hoehle` | Höhle | Level „Kurs A: Rechnen“, öffnet sich nach dem Berg |
| `stein` | Steinkreis | Mini-Spiel Tic-Tac-Toe |

4. **Welche Wege?** Zwischen welchen Orten kann man direkt gehen? Beispielwelt: Lager–Baumhaus, Baumhaus–See,
   Baumhaus–Berg, Berg–Höhle, See–Höhle, Lager–Steinkreis.
5. **In welcher Reihenfolge öffnen sich die Orte?** Beispielwelt: Baumhaus ist von Anfang an offen; der Berg öffnet sich,
   wenn das Baumhaus-Level mindestens einen Stern hat; die Höhle, wenn das Berg-Level einen Stern hat. Das ist die
   „Geschichte“ der Welt.

Wie viele Orte? Für den Anfang reichen vier bis sieben. Ihr könnt später immer mehr dazubauen (bis 60 Orte, 40 Level).

## Schritt 2: Male oder fotografiere die Karte

Die Karte darf **jeder Stil** sein: Buntstifte auf Papier und abfotografiert, am Tablet gemalt, Bastelkarte, ein
Foto eures Gartens mit Wegen. Wichtig sind nur wenige Dinge:

- **Format**: Querformat 4:3. Gut sind **2048 × 1536** oder **3072 × 2304** Pixel. Erlaubt ist 512 bis 8192 Pixel je Seite.
- **Dateityp**: JPEG (`.jpg`) oder PNG (`.png`), höchstens **8 MB**. Fotos als JPEG mit mittlerer bis hoher Qualität speichern.
- **Dateiname**: einfach, ohne Leerzeichen und Ordner, z. B. `karte.jpg`.
- **Keine Schrift im Bild.** Die Namen der Orte zeichnet die App selbst, **unter** den Standpunkt jedes Ortes. Lass dort Platz.
- **Gebäude oben, Standpunkt unten.** Der Standpunkt ist die Stelle, an der die beiden Figuren stehen. Male das Gebäude
  (Baumhaus, Berg, Höhle …) so, dass sein Fuß an diesem Punkt endet, und den Weg davor frei. Die Figuren stehen sonst mitten
  im Gebäude.
- **Wege** malen oder andeuten. Die App zieht beim Laufen Linien zwischen den Standpunkten; gemalte Wege, die ungefähr
  dazu passen, sehen am besten aus.
- Lass an den Standpunkten freie Flächen (Wiese, Pfad), damit die Figuren gut zu sehen sind.

Tipp: Zeichne zuerst nur die Wege und die Standpunkte als Punkte, lies dann die Koordinaten ab (Schritt 3) und male
erst danach die Gebäude darüber. Dann stimmt alles.

Speichere das Bild als `karte.jpg` in einen neuen Ordner. Der Ordnername ist die **Paket-ID**, zum Beispiel
`de.familie-muster.kurse` (mindestens drei Teile, Kleinbuchstaben, Ziffern und Bindestriche, durch Punkte getrennt):

```
packs/de.familie-muster.kurse/
  karte.jpg
  pack.json      (entsteht in Schritt 4)
```

## Schritt 3: Koordinaten der Orte ablesen

Jeder Ort bekommt `x` und `y` als **Bruchteil des Bildes**, von 0 bis 1:

- `x = Pixel von links ÷ Bildbreite`
- `y = Pixel von oben ÷ Bildhöhe`

So gehst du vor:
1. Öffne die Karte in einem Bildprogramm, das beim Überfahren mit der Maus die Pixelposition anzeigt (Vorschau auf dem Mac
   zeigt sie im Werkzeug „Auswahl“ beziehungsweise im Informationsfenster; GIMP, Affinity, Photoshop, Krita und viele
   Web-Bildeditoren können es auch). Die Position `0,0` ist die **obere linke** Ecke.
2. Fahre mit der Maus auf den **Standpunkt** jedes Ortes (an den Fuß des Gebäudes, auf den Weg) und notiere die Pixelposition.
3. Rechne um. Bei 2048 × 1536 Pixeln:

| Ort | Pixel (links, oben) | `x` = Pixel ÷ 2048 | `y` = Pixel ÷ 1536 |
|---|---|---|---|
| Lager | 410, 1229 | 0,20 | 0,80 |
| Baumhaus | 860, 891 | 0,42 | 0,58 |
| See | 1434, 1106 | 0,70 | 0,72 |
| Berg | 1270, 461 | 0,62 | 0,30 |
| Höhle | 1761, 707 | 0,86 | 0,46 |
| Steinkreis | 614, 522 | 0,30 | 0,34 |

Zwei Nachkommastellen genügen. Schreibe `0.42` (mit **Punkt**, nicht mit Komma) in die Datei.

Hast du ein anderes Seitenverhältnis oder eine andere Größe, ändert sich nur die Teilung: immer durch die **wirkliche**
Breite beziehungsweise Höhe des Bildes teilen, und dieselben Zahlen später unter `image.width` und `image.height`
eintragen.

## Schritt 4: Schreibe die `pack.json`

Lege die Datei neben die Karte. Beginne mit dem Gerüst. Das Beispiel zeigt die Beispielwelt (gekürzt):

```json
{
  "$schema": "../../docs/schema/pack.schema.json",
  "id": "de.familie-muster.kurse",
  "version": 1,
  "title": { "de": "Unsere Welt" },
  "description": { "de": "Für Klasse 4" },
  "author": "Familie Muster",
  "licence": "CC-BY-4.0",
  "courses": [],
  "skills": {},
  "world": {},
  "levels": []
}
```

Die ersten Zeilen: `$schema` lässt den Editor mitprüfen (siehe [FORMAT.md, Abschnitt 16](FORMAT.md#16-prüfen-editor-skript-app-prüfer)).
`version` erhöhst du bei jeder Änderung. `licence` sollte `CC-BY-4.0` sein, wenn ihr die Welt hier veröffentlichen
wollt.

### 4a. Kurse für eure Kinder definieren

Ein Kurs ist ein eigenes Fach der Welt. Die Beispielwelt für 9-Jährige:

```json
"courses": [
  { "id": "kurs-a", "title": { "de": "Kurs A: Rechnen", "en": "Course A: Maths" } },
  { "id": "kurs-b", "title": { "de": "Kurs B: Lesen",   "en": "Course B: Reading" } },
  { "id": "kurs-c", "title": { "de": "Kurs C: Natur",   "en": "Course C: Nature" } }
]
```

Die `id` besteht aus Kleinbuchstaben, Ziffern und `-` (höchstens 40 Zeichen) und darf nicht `math`, `german`, `science`
oder `english` heißen. Jedes Level gehört mit `"subject": "kurs-a"` zu einem Kurs. Wenn die Eltern das Paket
einschalten, sind seine Kurse an.

### 4b. Die Welt beschreiben

Die Beispielwelt, vollständig:

```json
"world": {
  "image": { "file": "karte.jpg", "width": 2048, "height": 1536 },
  "start": "lager",
  "nodes": [
    { "id": "lager",  "title": { "de": "Lager" },      "x": 0.20, "y": 0.80, "requires": [] },
    { "id": "baum",   "title": { "de": "Baumhaus" },   "level": "de.huckepack.beispielwelt/baumhaus", "x": 0.42, "y": 0.58, "requires": [] },
    { "id": "see",    "title": { "de": "See" },        "level": "de.huckepack.beispielwelt/see",     "x": 0.70, "y": 0.72, "requires": [] },
    { "id": "berg",   "title": { "de": "Berg" },       "level": "de.huckepack.beispielwelt/berg",    "x": 0.62, "y": 0.30,
      "requires": ["de.huckepack.beispielwelt/baumhaus"] },
    { "id": "hoehle", "title": { "de": "Höhle" },      "level": "de.huckepack.beispielwelt/hoehle",  "x": 0.86, "y": 0.46,
      "requires": ["de.huckepack.beispielwelt/berg"] },
    { "id": "stein",  "title": { "de": "Steinkreis" }, "miniGame": "ticTacToe", "x": 0.30, "y": 0.34, "requires": [] }
  ],
  "paths": [
    ["lager", "baum"], ["baum", "see"], ["baum", "berg"],
    ["berg", "hoehle"], ["see", "hoehle"], ["lager", "stein"]
  ]
}
```

Was hier passiert:
- `image` nennt die Karte und ihre **echten** Pixelmaße.
- `start` ist der Ort, an dem beide Figuren anfangen.
- Jeder Ort hat `x` und `y` aus Schritt 3, und **immer** ein `requires` (leer `[]`, wenn er von Anfang an offen ist).
- `level` verweist auf die ID eines Levels (Schritt 4c). `miniGame` (`ticTacToe` oder `dotsAndBoxes`) ist ein Spiel
  ohne Lernstoff. Ein Ort hat das eine **oder** das andere.
- `requires` zählt Level auf, die mindestens **einen Stern** haben müssen. Berg und Höhle öffnen sich also nacheinander.
- `paths` verbindet Orte, in beide Richtungen.

Gesperrte Orte kann man nicht durchqueren. In der Beispielwelt ist das unproblematisch: Zum Berg geht man nur über das
Baumhaus (das offen ist), zur Höhle über den See oder den Berg; sie selbst bleibt zu, bis das Berg-Level einen Stern hat.

### 4c. Level schreiben

Ein Level ist eine Kette von 4 bis 6 Aufgaben eines Kurses. Die Beispielwelt hat fünf Level:

| Level-ID | Ort | Kurs | Aufgabentypen |
|---|---|---|---|
| `…/baumhaus` | `baum` | `kurs-a` | splitInfo (mit Geld), relay, matchPairs, bothAgree |
| `…/baumhaus-2` | Band am `baum` | `kurs-a` | splitInfo (Analoguhr), relay (Zeit), matchPairs, bothAgree (Digitaluhren), splitInfo (Minuten) |
| `…/see` | `see` | `kurs-c` | splitInfo, matchPairs, bothAgree, relay |
| `…/berg` | `berg` | `kurs-b` | splitInfo, bothAgree, matchPairs, relay, bothAgree |
| `…/hoehle` | `hoehle` | `kurs-a` | splitInfo, relay (Geld), matchPairs, bothAgree (Geld-Bild), splitInfo |

Das Gerüst eines Levels (`…` steht für die Paket-ID):

```json
{
  "id": "de.familie-muster.kurse/baumhaus",
  "schemaVersion": 1,
  "title": { "de": "Das Baumhaus" },
  "subject": "kurs-a",
  "grade": 4,
  "tasks": [ ]
}
```

Die Level-ID muss mit der Paket-ID und einem Schrägstrich beginnen. Auf sie verweisen `level` und `requires` im
`world`-Teil.

**Aufgaben** schreibst du in `tasks`. Hier ein vollständiges Mini-Level, das alle vier Typen zeigt (in der Beispielwelt
siehst du mehr davon):

```json
"tasks": [
  {
    "id": "bh-1", "skills": ["kurs-a.rechnen.malnehmen"], "type": "splitInfo", "difficulty": 1,
    "clue":   { "de": "Im Baumhaus liegen 4 Stapel Bretter. In jedem Stapel sind 12 Bretter." },
    "prompt": { "de": "Wie viele Bretter liegen insgesamt im Baumhaus?" },
    "answer": 48
  },
  {
    "id": "bh-2", "skills": ["kurs-a.rechnen.addieren-subtrahieren"], "type": "relay",
    "first": { "de": "Rechne 36 + 28." }, "firstAnswer": 64,
    "operation": { "op": "subtract", "operand": 19 },
    "second": { "de": "Rechne {x} − 19." }
  },
  {
    "id": "bh-3", "skills": ["kurs-a.rechnen.malnehmen"], "type": "matchPairs",
    "prompt": { "de": "Welche Aufgabe passt zu welchem Ergebnis?" },
    "pairs": [
      { "left": { "de": "6 · 7" },  "right": { "de": "42" } },
      { "left": { "de": "8 · 9" },  "right": { "de": "72" } },
      { "left": { "de": "12 · 5" }, "right": { "de": "60" } }
    ]
  },
  {
    "id": "bh-4", "skills": ["kurs-a.rechnen.malnehmen"], "type": "bothAgree", "difficulty": 3,
    "question": { "de": "Welche Aufgabe hat das Ergebnis 240?" },
    "options": [
      { "id": "a", "text": { "de": "30 · 8" } },
      { "id": "b", "text": { "de": "24 · 8" } },
      { "id": "c", "text": { "de": "40 · 7" } }
    ],
    "correct": "a"
  }
]
```

Beim Schreiben jeder Aufgabe fragst du dich: **Warum braucht das eine Kind das andere?**

- `splitInfo`: Das eine Kind liest den Hinweis (mit allen Zahlen), das andere sieht nur die Frage und tippt die Antwort.
- `relay`: Das eine Kind löst Schritt 1; mit seinem Ergebnis rechnet das andere Schritt 2. Der Text von Schritt 2
  enthält `{x}` für dieses Ergebnis.
- `matchPairs`: Jedes Kind hält eine Hälfte jedes Paares; sie lesen sich ihre Karten vor und tippen passende
  zusammen.
- `bothAgree`: Beide sehen dieselbe Frage und müssen sich auf dieselbe richtige Antwort einigen.

Alle Felder, Grenzen und Antwortformate (Cent, Uhrzeit als Minuten seit Mitternacht, Dauer in Minuten) stehen in
[FORMAT.md, Abschnitt 6 bis 9](FORMAT.md#6-die-vier-aufgabentypen). Wie man gute Koop-Aufgaben schreibt, in
[Abschnitt 15](FORMAT.md#15-was-eine-gute-koop-aufgabe-ausmacht).

**Schwierigkeit:** Markiere ein, zwei schwere Aufgaben mit `"difficulty": 3`. Auf der Einstellung „Schwer“ werden sie
mitgespielt, bei „Normal“ und „Leicht“ übersprungen. „Leicht“ spielt höchstens die ersten vier Aufgaben. Schreibe also
mindestens vier Aufgaben mit `difficulty` 1 oder 2 in jedes Level.

**Ein zweites Level am selben Ort („Band“):** Gib dem Level ein `place` mit der ID des Ortes. Es erscheint, sobald das
erste Level dort einen Stern hat:

```json
{ "id": "de.familie-muster.kurse/baumhaus-2", "schemaVersion": 1, "place": "baum",
  "title": { "de": "Das Baumhaus: Uhrzeiten" }, "subject": "kurs-a", "grade": 4, "tasks": [ ] }
```

Der Ort `baum` muss ein eigenes Level (`nodes[].level`) haben. Level mit `place` darfst du **nicht** in `level` oder
`requires` eintragen.

**Fähigkeiten:** Jede Aufgabe hat `skills`, z. B. `kurs-a.rechnen.malnehmen`. Gib neuen Fähigkeiten im Paket einen
Namen, damit die Eltern-Auswertung sie anzeigt (Beispiel: `"skills": { "kurs-a.rechnen.malnehmen": { "de": "Malnehmen" } }`).

## Schritt 5: Prüfen

1. **Im Editor:** Mit der `$schema`-Zeile markiert Visual Studio Code Tippfehler und fehlende Felder sofort.
2. **Mit dem Skript** (nur Python 3 nötig), vom Hauptordner dieses Repositorys aus:
   ```
   python3 tools/check_format.py packs/de.familie-muster.kurse/pack.json
   ```
   Es prüft u. a., ob die Karte neben der `pack.json` liegt, ob die Maße stimmen, ob alle Orte, Wege und Level
   zusammenpassen und ob die Aufgaben die Regeln einhalten. Jede Meldung beginnt mit dem Ort des Fehlers.
3. **Ausprobieren:** Spielt die Welt zu zweit durch (nächster Schritt). Rechnet nach, ob alle Lösungen stimmen.
   Typische Fehler: ein Ort ohne `requires`, ein Level-Verweis mit Tippfehler, `second` ohne `{x}`, eine Uhrzeit als
   `1635` statt `995` (Minuten seit Mitternacht).

Die häufigsten Meldungen:

| Meldung | Ursache |
|---|---|
| `place 'x': 'requires' is required (use [])` | `"requires": []` fehlt |
| `... is not a level of this pack without 'place'` | `level` oder `requires` nennt eine falsche ID oder ein Band-Level |
| `image karte.jpg not found` | Bild liegt nicht neben der `pack.json` |
| `image ... is 2048x1536 px but pack.json says ...` | `width`/`height` stimmen nicht mit dem Bild |
| `'second' needs {x} in every language` | der Text von Schritt 2 enthält kein `{x}` |
| `subject '…' is neither built-in nor in 'courses'` | Kurs fehlt unter `courses` |

## Schritt 6: Installieren

1. Bringe den Ordner (mit `pack.json` **und** dem Kartenbild) auf das **Eltern-Gerät**, zum Beispiel über iCloud Drive
   oder „Dateien“.
2. In Huckepack auf dem Eltern-Gerät: **Eltern-Bereich › Fächer › „Paket hinzufügen …“**. Wähle den **Ordner** des Pakets,
   in dem `pack.json` und das Kartenbild liegen.
3. **Schalte das Paket ein.**
4. Sobald die Geräte der Kinder sich mit dem Eltern-Gerät verbinden, bekommen sie die Welt (mit dem Bild).
   Beide Kinder müssen das Paket bekommen haben.
5. Auf dem Startbildschirm der Kinder-Geräte wählen die beiden **gemeinsam** die Welt aus. Dann geht es los.

Wenn du die Welt später änderst: `version` um eins erhöhen und das Paket erneut hinzufügen.

## Schritt 7 (freiwillig): Teilen

Wollt ihr eure Welt für andere bereitstellen? Lest [CONTRIBUTING.md](../CONTRIBUTING.md). Dort stehen die Regeln
(eigene Aufgaben, richtig, Koop, nichts Persönliches) und wie ein Pull Request abläuft.
