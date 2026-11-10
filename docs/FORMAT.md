# Huckepack-Paketformat (`pack.json`)

*English summary: this is the complete reference for Huckepack content packs. A pack is a folder with a `pack.json`
(plus a map image for world packs). A **level pack** adds levels ("Band 2") to places of the Huckepack map; a **world
pack** brings its own map image, places, paths and courses for any age (grade 1 to 13). Every task needs both kids
(co-op on two devices). Four task types: `splitInfo`, `relay`, `matchPairs`, `bothAgree`. A JSON Schema is in
`docs/schema/pack.schema.json`; `tools/check_format.py` checks a pack without the app. The rest is in German.*

Diese Datei beschreibt jedes Feld. Wer eine eigene Welt bauen will, liest zuerst [WELT-ANLEGEN.md](WELT-ANLEGEN.md).
Das Beispiel `packs/de.huckepack.beispielwelt/pack.json` ist eine vollständige Welt und passt zu allem, was hier steht.

## Inhalt
1. [Die Grundidee: zwei Kinder, zwei Geräte](#1-die-grundidee-zwei-kinder-zwei-geräte)
2. [Ordner und Dateien](#2-ordner-und-dateien)
3. [Das Paket: Felder von `pack.json`](#3-das-paket-felder-von-packjson)
4. [Level](#4-level)
5. [Aufgaben: gemeinsame Felder](#5-aufgaben-gemeinsame-felder)
6. [Die vier Aufgabentypen](#6-die-vier-aufgabentypen)
7. [Bilder in Aufgaben (Visuals)](#7-bilder-in-aufgaben-visuals)
8. [Antwortformate](#8-antwortformate)
9. [Rechenschritt-Operationen (`relay`)](#9-rechenschritt-operationen-relay)
10. [Die Welt: `world`](#10-die-welt-world)
11. [Wie Orte aufgehen und wie „Band“ funktioniert](#11-wie-orte-aufgehen-und-wie-band-funktioniert)
12. [Texte in mehreren Sprachen](#12-texte-in-mehreren-sprachen)
13. [Fähigkeiten (`skills`)](#13-fähigkeiten-skills)
14. [Grenzen auf einen Blick](#14-grenzen-auf-einen-blick)
15. [Was eine gute Koop-Aufgabe ausmacht](#15-was-eine-gute-koop-aufgabe-ausmacht)
16. [Prüfen: Editor, Skript, App-Prüfer](#16-prüfen-editor-skript-app-prüfer)
17. [Checkliste vor dem Einreichen](#17-checkliste-vor-dem-einreichen)

---

## 1. Die Grundidee: zwei Kinder, zwei Geräte

Huckepack wird immer **zu zweit** gespielt, jedes Kind auf einem eigenen Gerät. Beide Avatare laufen gemeinsam über die
Karte von Ort zu Ort, und in jedem Level lösen sie Aufgaben, die **keines der beiden allein lösen kann**. Das ist der
Kern des Spiels: Die Kinder müssen miteinander reden, einander erklären, zuhören und sich einigen. Der Name ist
Programm: Eins trägt das andere „huckepack“.

Technisch heißt das: Jede Aufgabe verteilt das Wissen oder die Handgriffe auf beide Geräte. Welches Kind welche
Rolle hat, wechselt von Aufgabe zu Aufgabe, damit beide jede Rolle üben. Beide Geräte zeigen denselben Spielstand;
die Antwort wird vom Programm geprüft, nicht von einem Kind.

Beim Schreiben einer Aufgabe immer fragen: **Was sieht Gerät A, was sieht Gerät B, und warum muss A es B erzählen?**
Wenn ein Kind die Aufgabe allein auf seinem Bildschirm lösen könnte, ist es keine Koop-Aufgabe (siehe
[Abschnitt 15](#15-was-eine-gute-koop-aufgabe-ausmacht)).

## 2. Ordner und Dateien

```
packs/
  de.familie-muster.kurse/        Ordnername = Paket-ID
    pack.json                     die Beschreibung (höchstens 512 KB)
    karte.jpg                     nur bei Welt-Paketen: das Kartenbild (höchstens 8 MB)
```

- Der Ordnername ist die Paket-ID (Prüfskript und Konvention in diesem Repository).
- Das Kartenbild liegt **direkt neben** `pack.json`, nicht in einem Unterordner.
- Mehr Dateien kennt das Format nicht. Aufgaben bestehen nur aus Text und den eingebauten Bildern (Uhr, Geld).

Zwei Arten von Paketen, nur unterschieden durch das Feld `world`:

| | Level-Paket | Welt-Paket |
|---|---|---|
| `world` | fehlt | vorhanden |
| Karte | die Huckepack-Karte der App | eigenes Bild mit eigenen Orten und Wegen |
| `level.place` | **Pflicht**: ein Ort der Huckepack-Karte | optional: ein Ort der eigenen Welt (macht das Level zu „Band 2, 3 …“) |
| Fächer | `math`, `german`, `science`, `english` oder eigene `courses` | dasselbe, meist eigene `courses` |

## 3. Das Paket: Felder von `pack.json`

```json
{
  "$schema": "../../docs/schema/pack.schema.json",
  "id": "de.familie-muster.kurse",
  "version": 1,
  "title": { "de": "Kurse für Klasse 4", "en": "Courses for grade 4" },
  "description": { "de": "Rechnen, Lesen und Natur (ab 8 Jahren)" },
  "author": "Familie Muster",
  "licence": "CC-BY-4.0",
  "courses": [ { "id": "kurs-a", "title": { "de": "Kurs A: Rechnen" } } ],
  "skills": { "kurs-a.rechnen.malnehmen": { "de": "Malnehmen" } },
  "world": { "...": "siehe Abschnitt 10" },
  "levels": [ { "...": "siehe Abschnitt 4" } ]
}
```

| Feld | Pflicht | Typ | Regel |
|---|---|---|---|
| `$schema` | nein | Text | Nur ein Hinweis für Editoren (siehe [Abschnitt 16](#16-prüfen-editor-skript-app-prüfer)). Die App ignoriert ihn. |
| `id` | ja | Text | Mindestens **drei** Teile, durch Punkte getrennt; jeder Teil besteht nur aus Kleinbuchstaben `a–z`, Ziffern und `-`, z. B. `de.familie-muster.kurse`. Die ID ist weltweit eindeutig gedacht: erster Teil Sprache oder Land, zweiter Teil du, dritter Teil das Thema. |
| `version` | ja | ganze Zahl ≥ 1 | Bei **jeder** Änderung erhöhen. Eine neuere Version eines eingeschalteten Pakets ersetzt die alte auch bei den Kindern. |
| `title` | ja | [Text](#12-texte-in-mehreren-sprachen) | Name des Pakets (Eltern-Bereich, Weltauswahl). |
| `description` | nein | Text | Ein Satz für Eltern, z. B. „für 8–10 Jahre“. |
| `author` | ja | Text | Name oder Gruppe. Keine echten Namen von Kindern. |
| `licence` | ja | Text | Für Pakete in diesem Repository: `CC-BY-4.0`. |
| `courses` | nein | Liste | Eigene Kurse (Fächer), siehe unten. Nötig, sobald ein Level ein anderes Fach als die vier eingebauten hat. |
| `skills` | nein | Objekt | Namen für Fähigkeiten, siehe [Abschnitt 13](#13-fähigkeiten-skills). |
| `world` | nein | Objekt | Macht das Paket zum Welt-Paket, siehe [Abschnitt 10](#10-die-welt-world). |
| `levels` | ja | Liste | 1 bis **40** Level, siehe [Abschnitt 4](#4-level). |

Die Datei darf höchstens **512 KB** groß sein (sie reist als eine Nachricht im Heimnetz vom Eltern-Gerät zu den
Kinder-Geräten).

### Kurse (`courses`)

Ein Kurs ist ein eigenes Fach des Pakets: „Kurs A“, „Dinosaurier“, „Latein“. Jedes Level gehört zu genau einem Fach.

| Feld | Pflicht | Regel |
|---|---|---|
| `id` | ja | Kleinbuchstaben, Ziffern, `-`, höchstens 40 Zeichen. Darf **nicht** `math`, `german`, `science` oder `english` heißen. Eindeutig im Paket. |
| `title` | ja | Text, der Eltern und Kindern gezeigt wird. |

Die vier eingebauten Fächer brauchen keinen Eintrag. Ein Level darf deshalb `"subject": "math"` haben, ohne dass
`courses` es nennt. Hinweis für Welt-Pakete: Eingebaute Fächer kann der Elternteil in den Einstellungen ein- und
ausschalten, und ein abgeschalteter Ort mit einem Level dieses Fachs lässt sich nicht betreten. Eigene Kurse sind
dagegen eingeschaltet, solange das Paket eingeschaltet ist. Für eine Welt mit eigenen Kursen deshalb eigene
Kurs-IDs verwenden.

## 4. Level

Ein Level ist eine kurze Kette von Aufgaben **eines** Fachs, die man an einem Ort der Karte betritt. Gut sind 4 bis 6
Aufgaben (rund 5 bis 10 Minuten).

```json
{
  "id": "de.familie-muster.kurse/baumhaus",
  "schemaVersion": 1,
  "title": { "de": "Das Baumhaus" },
  "subject": "kurs-a",
  "grade": 4,
  "place": "baum",
  "tasks": [ ]
}
```

| Feld | Pflicht | Regel |
|---|---|---|
| `id` | ja | Muss mit `<Paket-ID>/` beginnen, danach mindestens ein Zeichen (z. B. `de.familie-muster.kurse/baumhaus`). Eindeutig im Paket. Auf diese ID verweisen `world.nodes[].level` und `requires`. |
| `schemaVersion` | nein | `1` (Standard, wenn das Feld fehlt). |
| `title` | ja | Text. |
| `subject` | ja | `math`, `german`, `science`, `english` oder die ID eines Kurses aus `courses`. |
| `grade` | ja | Ganze Zahl **1 bis 13** (Klassenstufe, nur zur Orientierung). |
| `place` | siehe Tabelle in Abschnitt 2 | Macht das Level zu einem **weiteren Level an einem Ort** („Band“). Siehe [Abschnitt 11](#11-wie-orte-aufgehen-und-wie-band-funktioniert). |
| `tasks` | ja | Mindestens eine Aufgabe, jede `id` nur einmal im Level. |

### Orte der Huckepack-Karte (Level-Pakete)

Ein Level-Paket nennt in `place` einen Ort der Huckepack-Karte, an dem das Level als nächster „Band“ erscheint:
`numbers-hill`, `mill`, `market`, `clock-tower`, `syllable-school`, `library`, `post-office`, `farm`,
`weather-station`, `crossing`, `bus-stop`, `tea-house`, `zoo`, `lighthouse`.

## 5. Aufgaben: gemeinsame Felder

Jede Aufgabe ist ein Objekt in `tasks`. Diese Felder haben alle vier Typen:

| Feld | Pflicht | Regel |
|---|---|---|
| `id` | ja | Text, eindeutig **im Level** (z. B. `bh-1`). |
| `type` | ja | `splitInfo`, `relay`, `matchPairs` oder `bothAgree`. |
| `skills` | ja | Liste mit mindestens einer [Fähigkeits-ID](#13-fähigkeiten-skills), z. B. `["kurs-a.rechnen.malnehmen"]`. |
| `difficulty` | nein | `1` leicht, `2` normal (Standard, wenn das Feld fehlt), `3` schwer. |

### Was „Leicht / Normal / Schwer“ im Eltern-Bereich macht

Der Elternteil stellt die Schwierigkeit für die Kinder ein. Die App wählt daraus die Aufgaben eines Levels so aus:

| Einstellung | Gespielte Aufgaben |
|---|---|
| Leicht | alle mit `difficulty` 1 oder 2, aber **höchstens die ersten vier** (in der Reihenfolge der Liste) |
| Normal | alle mit `difficulty` 1 oder 2 |
| Schwer | **alle**, auch die mit `difficulty` 3 |

Folgen für dich:
- Schreibe in jedes Level mindestens **vier** Aufgaben mit `difficulty` 1 oder 2, sonst spielt „Leicht“ weniger und
  ein Level, dessen Aufgaben alle `3` sind, spielt bei „Leicht“ und „Normal“ gar nichts. Das Prüfskript meldet das.
- `difficulty` 1 gibt es als Kennzeichnung, gespielt wird es wie `2`. Sortiere die leichtesten Aufgaben nach vorn.
- Die Reihenfolge der Liste ist die Spielreihenfolge. Der Anfang sollte leichter sein als das Ende.

Stern-Wertung eines Levels: keine Fehler = 3 Sterne, bis zu 2 Fehler = 2 Sterne, sonst 1 Stern. Fehler zählen über das
ganze Level. Nach dem Level behalten die Kinder den besten Wert.

## 6. Die vier Aufgabentypen

Alle Texte sind [LocalizedText](#12-texte-in-mehreren-sprachen). Welches Kind welche Rolle bekommt, wechselt von
Aufgabe zu Aufgabe; im Folgenden heißen sie nach der Rolle.

### 6.1 `splitInfo` – Hinweis und Eingabe getrennt

Ein Kind sieht den **Hinweis** und muss ihn dem anderen mündlich weitergeben. Das andere Kind sieht nur die **Frage**
und tippt die Zahl ein.

| Feld | Pflicht | Regel |
|---|---|---|
| `clue` | ja | Hinweistext. **Nur** das Hinweis-Kind sieht ihn. Er muss alle Zahlen und Angaben enthalten. |
| `clueVisual` | nein | [Bild](#7-bilder-in-aufgaben-visuals) (Uhr, Geld), ebenfalls nur beim Hinweis-Kind. |
| `prompt` | ja | Frage. **Nur** das Eingabe-Kind sieht sie, dazu das Ziffernfeld. |
| `answer` | ja | Die Lösung als ganze Zahl (nicht negativ), siehe [Antwortformate](#8-antwortformate). |
| `answerFormat` | nein | `integer` (Standard), `euroCents`, `time`, `minutes`. |

Wer sieht was:

| | Hinweis-Kind | Eingabe-Kind |
|---|---|---|
| `clue`, `clueVisual` | ja | nein |
| `prompt`, Ziffernfeld | nein | ja |

Regeln: Bei `answerFormat: "time"` muss `answer` zwischen 0 und 1439 liegen.

Die Frage soll **ohne** den Hinweis nicht beantwortbar sein, und der Hinweis soll **ohne** die Frage nicht schon alles
verraten. Gute Aufgaben fragen nach etwas, das erst aus dem Hinweis berechnet oder abgelesen wird.

```json
{
  "id": "bh-5",
  "skills": ["kurs-a.geld.zaehlen"],
  "type": "splitInfo",
  "clue": { "de": "Du siehst das Geld aus der Spardose. Sag deinem Partner, welche Münzen und Scheine es sind." },
  "clueVisual": { "money": { "cents": [200, 100, 50, 20, 5] } },
  "prompt": { "de": "Wie viel Geld ist in der Spardose? Tippt den Betrag." },
  "answer": 375,
  "answerFormat": "euroCents"
}
```

(200 + 100 + 50 + 20 + 5 Cent = 375 Cent = 3,75 €.)

### 6.2 `relay` – Staffel in zwei Rechenschritten

Kind 1 löst Schritt 1. Das Ergebnis geht automatisch an Kind 2, das damit Schritt 2 löst. Kind 2 sieht Schritt 2 erst
mit dem fertigen Ergebnis von Kind 1 im Text.

| Feld | Pflicht | Regel |
|---|---|---|
| `first` | ja | Text von Schritt 1 (nur Kind 1). |
| `firstAnswer` | ja | Lösung von Schritt 1, ganze Zahl ≥ 0. |
| `operation` | ja | Wie aus `firstAnswer` die Lösung von Schritt 2 wird, siehe [Abschnitt 9](#9-rechenschritt-operationen-relay). |
| `second` | ja | Text von Schritt 2. Muss in **jeder** Sprache genau dort `{x}` enthalten, wo das Ergebnis von Schritt 1 stehen soll. |
| `answerFormat` | nein | Format **beider** Antworten und von `{x}` im Text, z. B. `euroCents` oder `time`. |

Wer sieht was:

| | Kind 1 | Kind 2 |
|---|---|---|
| zuerst | `first` und Ziffernfeld | sieht `second` mit „…“ statt `{x}` und wartet |
| nach Schritt 1 | sieht `second` mit eingesetztem Ergebnis (nur lesen) | `second` mit eingesetztem Ergebnis und Ziffernfeld |

Die Lösung von Schritt 2 ist `operation` angewendet auf `firstAnswer`. Du schreibst sie **nicht** selbst ins JSON; deshalb
muss `second` zur Operation passen. `{x}` wird im gewählten Format angezeigt (bei `euroCents` als `7,00 €`, bei `time`
als `15:30`).

Regeln: Bei `divide` darf der Operand nicht 0 sein und `firstAnswer` muss glatt durch ihn teilbar sein. Beide Antworten
müssen mit dem Ziffernfeld eintippbar sein, also nicht negativ (bei `time` zwischen 0 und 1439). Das Prüfskript
meldet beides; die App prüft die Eintippbarkeit des zweiten Ergebnisses nicht selbst.

Der Reiz liegt darin, dass Kind 2 auf Kind 1 **angewiesen** ist und Kind 1 sorgfältig sein muss. Schritt 1 darf
deshalb nicht trivial, aber auch nicht länger als Schritt 2 sein.

```json
{
  "id": "ho-2",
  "skills": ["kurs-a.geld.rechnen"],
  "type": "relay",
  "first": { "de": "Eine Taschenlampe kostet 3,50 €. Ihr kauft 2 Stück. Was kosten sie zusammen?" },
  "firstAnswer": 700,
  "operation": { "op": "subtract", "operand": 150 },
  "second": { "de": "Die Rechnung ist {x}. Ihr bekommt 1,50 € Rabatt. Wie viel zahlt ihr am Ende?" },
  "answerFormat": "euroCents"
}
```

(Schritt 1: 7,00 € = 700 Cent. Schritt 2: 700 − 150 = 550 Cent = 5,50 €.)

### 6.3 `matchPairs` – Paare mit geteilten Hälften

Jedes Kind hält **eine Hälfte jedes Paares**: Kind 1 alle linken Hälften, Kind 2 alle rechten, jeweils in
zufälliger (aber auf beiden Geräten gleicher) Reihenfolge. Die Kinder tippen je eine Karte an; stimmt das Paar, verschwinden
beide Karten, sonst zählt ein Fehler und beide Auswahlen werden zurückgesetzt. Weil keiner die Karten des anderen
sieht, müssen die Kinder sich ihre Karten **vorlesen und beschreiben**.

| Feld | Pflicht | Regel |
|---|---|---|
| `prompt` | ja | Anweisung, beide Kinder sehen sie. |
| `pairs` | ja | **2 bis 6** Paare. |
| `pairs[].left` | ja | Text der linken Hälfte (Kind 1). |
| `pairs[].right` | ja | Text der rechten Hälfte (Kind 2). |
| `pairs[].leftVisual` | nein | [Bild](#7-bilder-in-aufgaben-visuals) über dem Text der linken Karte. |
| `pairs[].rightVisual` | nein | Bild über dem Text der rechten Karte. |

Regeln: Alle `left`-Texte sind verschieden, alle `right`-Texte sind verschieden (sonst ist die Zuordnung nicht eindeutig).
Auch mit Bild braucht jede Karte einen Text.

```json
{
  "id": "bh-3",
  "skills": ["kurs-a.rechnen.malnehmen"],
  "type": "matchPairs",
  "prompt": { "de": "Welche Aufgabe passt zu welchem Ergebnis?" },
  "pairs": [
    { "left": { "de": "6 · 7" },  "right": { "de": "42" } },
    { "left": { "de": "8 · 9" },  "right": { "de": "72" } },
    { "left": { "de": "12 · 5" }, "right": { "de": "60" } },
    { "left": { "de": "25 · 4" }, "right": { "de": "100" } }
  ]
}
```

### 6.4 `bothAgree` – gemeinsame Entscheidung

Beide Kinder sehen **dieselbe** Frage mit denselben Antworten und wählen jeweils eine. Erst wenn beide gewählt haben,
wird geprüft: Die Aufgabe ist nur gelöst, wenn **beide** die richtige Antwort gewählt haben. Sonst zählt ein Fehler und
beide wählen neu. Die Kinder sollen also vorher darüber sprechen.

| Feld | Pflicht | Regel |
|---|---|---|
| `question` | ja | Frage (beide sehen sie). |
| `questionVisual` | nein | [Bild](#7-bilder-in-aufgaben-visuals) zur Frage. |
| `options` | ja | **2 bis 4** Antworten. |
| `options[].id` | ja | Kurzer Text (z. B. `a`), eindeutig in der Aufgabe. |
| `options[].text` | ja | Antworttext. |
| `options[].visual` | nein | Bild zur Antwort (z. B. eine Digitaluhr). |
| `correct` | ja | Die `id` der richtigen Antwort. Genau eine Antwort ist richtig. |

Wer sieht was: beide Kinder alles. Die Koop-Wirkung entsteht allein durch die Absprache; deshalb eignet sich der
Typ für Fragen, bei denen man sich **begründen** muss, nicht für Ja/Nein-Raten (siehe
[Abschnitt 15](#15-was-eine-gute-koop-aufgabe-ausmacht)). Verteile die richtige Antwort über `a`, `b`, `c`, `d`, damit sie nicht immer an derselben Stelle steht.

```json
{
  "id": "ho-4",
  "skills": ["kurs-a.geld.zaehlen"],
  "type": "bothAgree",
  "question": { "de": "Wie viel Geld ist das?" },
  "questionVisual": { "money": { "cents": [500, 200, 50, 10] } },
  "options": [
    { "id": "a", "text": { "de": "7,60 €" } },
    { "id": "b", "text": { "de": "6,70 €" } },
    { "id": "c", "text": { "de": "7,06 €" } }
  ],
  "correct": "a"
}
```

## 7. Bilder in Aufgaben (Visuals)

Die App zeichnet Uhren und Geld aus Daten. Ein Visual ist ein Objekt mit **genau einem** Schlüssel:

| Visual | JSON | Regel |
|---|---|---|
| Analoguhr | `{ "clock": { "hour": 15, "minute": 45 } }` | `hour` 0–23 (die Uhr zeigt `hour` modulo 12, also 15 wird als 3 Uhr gezeichnet), `minute` 0–59 |
| Digitaluhr | `{ "digitalClock": { "hour": 7, "minute": 5 } }` | gleiche Grenzen; angezeigt als `07:05` |
| Geld | `{ "money": { "cents": [200, 50, 5] } }` | 1 bis 12 Werte in Cent, jeder aus: 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000 (Münzen und Scheine); sie werden in der angegebenen Reihenfolge gezeichnet |

Wo ein Visual stehen darf:

| Aufgabe | Feld | Wer sieht es |
|---|---|---|
| `splitInfo` | `clueVisual` | nur das Hinweis-Kind |
| `matchPairs` | `pairs[].leftVisual`, `pairs[].rightVisual` | das Kind mit dieser Hälfte |
| `bothAgree` | `questionVisual`, `options[].visual` | beide |
| `relay` | – | (kein Visual möglich) |

Eine Analoguhr sagt nicht, ob es vormittags oder nachmittags ist; schreibe das in den Text, wenn es zählt („nachmittags“).

```json
{ "clueVisual": { "clock": { "hour": 15, "minute": 45 } } }
```

```json
{ "options": [ { "id": "a", "text": { "de": "Uhr A" }, "visual": { "digitalClock": { "hour": 8, "minute": 45 } } } ] }
```

## 8. Antwortformate

Antworten sind immer **ganze Zahlen, nicht negativ**. `answerFormat` bestimmt, wie die Kinder tippen und wie die Zahl
im JSON steht.

| `answerFormat` | Kinder tippen | Anzeige | Im JSON | Höchstens |
|---|---|---|---|---|
| `integer` (Standard) | Ziffern, z. B. `48` | `48` | `48` | 5 Ziffern (99999) |
| `euroCents` | Ziffern, die als Cent gelten; das Feld zeigt sofort `3,75 €` | `3,75 €` | **Cent**: `375` | 6 Ziffern (9999,99 €) |
| `time` | genau 4 Ziffern `hhmm`, z. B. `1635`; das Feld zeigt `16:35` | `16:35` | **Minuten seit Mitternacht**: `16 · 60 + 35 = 995` | 0 bis 1439 (23:59); „keine Uhrzeit“, wenn Stunde > 23 oder Minute > 59 |
| `minutes` | Ziffern, z. B. `570` | `9 h 30 min` (ab 60 zeigt das Feld die Umrechnung) | **Minuten**: `570` | 4 Ziffern (9999) |

Beispiele:
- 5,50 € → `"answer": 550, "answerFormat": "euroCents"`
- 7:05 Uhr → `"answer": 425, "answerFormat": "time"`
- 1 h 20 min → `"answer": 80, "answerFormat": "minutes"`
- 0,87 € → `87` (die Kinder tippen `87`)

Bei `euroCents` können die Kinder keine Komma-Taste benutzen: Sie tippen die Cent. Das Beispiel „3,75 €“ ist also die
Eingabe `375`. Bei `time` zählt auch eine führende Null: `7:05` wird `0705` getippt.

Das gewählte Format gilt auch für die Anzeige in `relay.second` (`{x}`). Ein Antworttext in einem Text (etwa „Der Zug
kommt um 10:15 an“) schreibst du selbst in der Schreibweise, die die Kinder sehen sollen.

## 9. Rechenschritt-Operationen (`relay`)

`operation` ist ein Objekt `{ "op": …, "operand": … }`. Es gilt: Lösung von Schritt 2 = `op` angewendet auf `firstAnswer`.

| `op` | Rechnung | Beispiel |
|---|---|---|
| `add` | `firstAnswer + operand` | `{ "op": "add", "operand": 45 }`: 930 → 975 |
| `subtract` | `firstAnswer − operand` | `{ "op": "subtract", "operand": 19 }`: 64 → 45 |
| `multiply` | `firstAnswer · operand` | `{ "op": "multiply", "operand": 2 }`: 3 → 6 |
| `divide` | `firstAnswer : operand` | `{ "op": "divide", "operand": 3 }`: 18 → 6 (muss glatt aufgehen, Operand ≠ 0) |

`operand` ist eine ganze Zahl. Achte darauf, dass `second` im Text dieselbe Rechnung beschreibt wie die Operation.
Bei Zeiten und Geld stehen `firstAnswer` und `operand` in der Einheit des Formats (Minuten beziehungsweise Cent).

```json
{
  "id": "bu-2",
  "skills": ["kurs-a.zeitspannen.rechnen"],
  "type": "relay",
  "first": { "de": "Die Bastelgruppe beginnt um 14:20 Uhr und dauert 1 Stunde und 10 Minuten. Wann ist sie zu Ende?" },
  "firstAnswer": 930,
  "operation": { "op": "add", "operand": 45 },
  "second": { "de": "Die Bastelgruppe ist um {x} zu Ende. Danach braucht ihr 45 Minuten zum Aufräumen. Wann seid ihr fertig?" },
  "answerFormat": "time"
}
```

(14:20 + 1:10 = 15:30 = 930 Minuten; plus 45 Minuten = 975 = 16:15.)

## 10. Die Welt: `world`

Ein Paket mit `world` bringt eine **eigene Karte**. Die Kinder wählen die Welt auf ihrem Startbildschirm gemeinsam
aus; dann gehören Karte, Orte und Level zu dieser Welt. Eine Welt wird immer allein gespielt: Ein Welt-Paket kann
keine Level zu einer anderen Welt hinzufügen, und ein Level-Paket kann keine Level zu deiner Welt hinzufügen.

```json
"world": {
  "image": { "file": "karte.jpg", "width": 2048, "height": 1536 },
  "start": "lager",
  "nodes": [
    { "id": "lager", "title": { "de": "Lager" }, "x": 0.20, "y": 0.80, "requires": [] },
    { "id": "baum", "title": { "de": "Baumhaus" }, "level": "de.familie-muster.kurse/baumhaus", "x": 0.42, "y": 0.58, "requires": [] }
  ],
  "paths": [ ["lager", "baum"] ]
}
```

### 10.1 Das Kartenbild (`image`)

| Feld | Pflicht | Regel |
|---|---|---|
| `file` | ja | Dateiname **neben** `pack.json`, ohne Ordner, nicht mit `.` beginnend. Endung `.jpg`, `.jpeg` oder `.png` (Groß-/Kleinschreibung egal). |
| `width` | ja | Breite des Bildes in Pixeln, 512 bis 8192. |
| `height` | ja | Höhe in Pixeln, 512 bis 8192. |

- Die Datei darf höchstens **8 MB** groß sein.
- `width` und `height` sollen die **echten** Pixelmaße sein. Das Prüfskript vergleicht sie mit der Datei; die App
  rechnet mit den Zahlen aus `pack.json`.
- Empfehlung: Querformat 4:3, z. B. 2048 × 1536 oder 3072 × 2304. Das passt gut auf iPad-Bildschirme. Zu stark
  abweichende Seitenverhältnisse werden mit Rändern gezeigt.
- JPEG für gemalte oder fotografierte Karten (kleiner), PNG für Zeichnungen mit großen Farbflächen.
- Das Bild darf keine Schrift enthalten, auf die es ankommt: Ortsnamen zeichnet die App selbst (siehe unten).

### 10.2 Koordinaten

`x` und `y` sind **Bruchteile des Bildes** von 0 bis 1:
- `x = 0` ist der linke, `x = 1` der rechte Bildrand.
- `y = 0` ist der **obere**, `y = 1` der untere Bildrand (wie in Bildbearbeitungsprogrammen, die Null oben links).

Aus Pixeln: `x = Pixel-x ÷ width`, `y = Pixel-y ÷ height`. Bei 2048 × 1536 liegt der Punkt (860, 891) bei
`x = 0.42`, `y = 0.58`.

Der Punkt ist der **Standpunkt**: Hier stehen die beiden Avatare, wenn sie an diesem Ort sind (der „Trittstein“ vor
dem Ort). Daraus folgt für das Malen:
- Das **Gebäude oder Wahrzeichen** des Ortes wird **über** diesem Punkt gemalt. Der Punkt liegt an seinem Fuß, auf dem
  Weg davor.
- Die **Beschriftung** (der Ortsname aus `title`) zeichnet die App **unterhalb** des Punktes. Lass dort Platz und male
  keine Schrift ins Bild.
- Die Avatare sollen auf einer freien Fläche stehen, nicht auf einer Mauer oder im Wasser.

Du musst die Orte nicht genau treffen, aber die Wege (`paths`) werden als Linien zwischen den Standpunkten gezogen;
die Karte sieht besser aus, wenn deine gemalten Wege dazu passen.

### 10.3 Orte (`nodes`)

1 bis **60** Orte.

| Feld | Pflicht | Regel |
|---|---|---|
| `id` | ja | Text, eindeutig in der Welt (z. B. `baum`). |
| `title` | nein | Name, den die App unter dem Ort zeigt. |
| `level` | nein | Level, das an diesem Ort gespielt wird: die `id` eines Levels **dieses Pakets, das kein `place` hat**. |
| `miniGame` | nein | `ticTacToe` oder `dotsAndBoxes`. Ein Spiel zwischendurch, kein Lernstoff. |
| `x`, `y` | ja | Standpunkt, 0 bis 1 (siehe oben). |
| `requires` | nein | Liste von Level-IDs, die **mindestens einen Stern** haben müssen, bevor der Ort sich öffnet. Fehlt das Feld, ist der Ort ohne Bedingung offen. |

Regeln:
- Ein Ort hat **nicht** gleichzeitig `level` und `miniGame`. Ein Ort ohne beides ist nur ein Rastplatz (z. B. das Lager).
- `requires` darf nur Level nennen, die dieses Paket enthält **und die kein `place` haben**. Ein Band-Level kann nicht
  verlangt werden.
- Kein Level wird von zwei Orten betreten: Das prüft die App nicht, es wäre aber verwirrend.
- Ein Level ohne `place`, auf das kein Ort zeigt, wird nie gespielt.

### 10.4 Wege (`paths`) und Start

- `paths` ist eine Liste von Paaren zweier Orts-IDs: `["lager", "baum"]`. Wege gelten **in beide Richtungen**.
- Die Avatare laufen nur über Wege, immer auf dem kürzesten Weg zum gewählten Ziel.
- `start` ist die ID des Ortes, an dem beide Avatare beginnen. Meist ein Ort ohne Level (Lager, Zuhause).
- Jeder Ort sollte über Wege erreichbar sein. Die Prüfung verlangt es nicht, ein nicht erreichbarer Ort kann aber nie
  betreten werden.
- Die Kinder gehen **nur über offene Orte**. Ein gesperrter Ort (wegen `requires`) kann auch nicht durchquert
  werden. Plane die Wege so, dass dahinterliegende Orte nicht allein über einen gesperrten Ort erreichbar sind, solange
  er gesperrt ist, oder nimm das bewusst als Spielidee („hinter dem Berg“).

## 11. Wie Orte aufgehen und wie „Band“ funktioniert

**Orte öffnen sich so:**
1. Ein Ort ist **offen**, wenn alle Level in seinem `requires` mindestens **einen Stern** haben (ein Level mit 1, 2 oder
   3 Sternen zählt). Bei `[]` ist er von Anfang an offen.
2. Hat der Ort ein Level, muss zusätzlich dessen Fach eingeschaltet sein (eingebaute Fächer schaltet der Elternteil
   ein und aus; eigene Kurse sind an, solange das Paket an ist).
3. Gesperrte Orte erscheinen auf der Karte, aber die Kinder können nicht hin.

**Bänder („Band 2, 3 …“) an einem Ort:** Ein Ort hat sein eigenes Level (`nodes[].level`, das erste). Weitere Level
desselben Ortes werden über das Feld `place` im **Level** angehängt:

```json
{ "id": "de.familie-muster.kurse/baumhaus-2", "schemaVersion": 1, "place": "baum", "subject": "kurs-a", "...": "..." }
```

- `place` ist die ID des Ortes. Bei einem Level-Paket ein Ort der Huckepack-Karte (Liste in Abschnitt 4), bei einem
  Welt-Paket ein Ort deiner Welt, **der ein eigenes Level hat**.
- Die Level eines Ortes stehen in dieser Reihenfolge: zuerst das Level des Ortes selbst, danach die Band-Level
  nach ihrer `id` sortiert (Pakete nach ihrer ID). Wähle die IDs so, dass die Sortierung stimmt, z. B.
  `baumhaus`, `baumhaus-2`, `baumhaus-3`.
- Jedes Band öffnet sich erst, wenn das Level **davor** am selben Ort mindestens einen Stern hat. Die Kinder
  wählen am Ort, welches der offenen Level sie spielen wollen.
- Ein Band-Level hat kein eigenes `requires`: Seine einzige Bedingung ist das Level davor. Möchtest du, dass ein
  Level an einem anderen Ort ein Band verlangt, geht das nicht; plane stattdessen ein neues Level mit eigenem Ort.
- Die Fächer der Level an einem Ort dürfen verschieden sein.

## 12. Texte in mehreren Sprachen

Jeder sichtbare Text ist ein Objekt mit Sprachcodes:

```json
{ "de": "Wie viele Bretter?", "en": "How many boards?" }
```

- `de` (Deutsch) ist in diesem Repository **Pflicht**. Die App fällt notfalls auf eine vorhandene Sprache zurück, das Prüfskript und das Schema
  verlangen aber `de`.
- `en` ist erwünscht, die App zeigt es, wenn das Gerät Englisch eingestellt hat.
- Andere Sprachcodes (`fr`, `tr`, …) sind erlaubt.
- Bei `relay.second` muss `{x}` in **jeder** angegebenen Sprache vorkommen.
- Keine Emojis, keine Links.

## 13. Fähigkeiten (`skills`)

Jede Aufgabe nennt in `skills`, was sie übt. Die Eltern-Auswertung zeigt, welche Fähigkeiten gut und welche noch schwer
sind.

- Format: **mindestens zwei** Teile mit Punkten, jeder Teil aus Kleinbuchstaben, Ziffern und `-`: `kurs-a.rechnen.malnehmen`.
- Der **erste** Teil soll das Fach beziehungsweise der Kurs sein (`math`, `kurs-a` …). Die App liest daraus das Fach der Fähigkeit.
- Bekannte Fähigkeiten der eingebauten Level (z. B. `math.mental.add-hundreds`) darfst du wiederverwenden; die Namen
  stehen in der App.
- Neue Fähigkeiten bekommen im Paket einen Namen für die Eltern-Auswertung:

```json
"skills": {
  "kurs-a.rechnen.malnehmen": { "de": "Malnehmen", "en": "Multiplication" }
}
```

Die App prüft nicht, ob jede verwendete Fähigkeit einen Namen hat. Das Prüfskript und der Menschen-Review schon: Gib allen neuen
Fähigkeiten einen Namen.

## 14. Grenzen auf einen Blick

| Was | Grenze |
|---|---|
| `pack.json` | höchstens 512 KB |
| Kartenbild | höchstens 8 MB, `.jpg`, `.jpeg` oder `.png`, 512 bis 8192 Pixel je Seite |
| Level je Paket | 1 bis 40 |
| Orte je Welt | 1 bis 60 |
| Aufgaben je Level | mindestens 1 (empfohlen 4 bis 6) |
| `grade` | 1 bis 13 |
| `difficulty` | 1, 2 oder 3 |
| `matchPairs` | 2 bis 6 Paare |
| `bothAgree` | 2 bis 4 Antworten |
| `money.cents` | 1 bis 12 Werte aus 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000 |
| Kurs-ID | Kleinbuchstaben, Ziffern, `-`, höchstens 40 Zeichen, nicht `math`/`german`/`science`/`english` |
| Paket-ID | mindestens drei Teile `a.b.c` (Kleinbuchstaben, Ziffern, `-`) |
| Antworten | ganze Zahlen ≥ 0 (siehe Abschnitt 8) |
| `schemaVersion` | 1 |

## 15. Was eine gute Koop-Aufgabe ausmacht

**Prinzip: Jedes Kind besitzt etwas, das dem anderen fehlt, und die Lösung braucht beides.** Außerdem soll das Reden
selbst etwas lernen lassen: beschreiben, vorlesen, nachfragen, begründen.

Gut:
- `splitInfo`: „Im Baumhaus liegen 4 Stapel Bretter, in jedem 12 Bretter.“ (Hinweis) / „Wie viele Bretter liegen
  insgesamt im Baumhaus?“ (Frage). Das eine Kind kennt die Zahlen, das andere die Frage. Ohne einander geht es nicht.
- `splitInfo` mit Visual: Ein Kind sieht eine Uhr oder Münzen und muss sie **beschreiben** („der kleine Zeiger steht kurz
  vor der 4“), das andere tippt die Uhrzeit oder den Betrag. Das übt Sprache und Fachbegriffe.
- `relay`: Schritt 2 braucht wirklich das Ergebnis von Schritt 1; Kind 1 trägt Verantwortung, Kind 2 muss ihm
  vertrauen oder nachfragen.
- `matchPairs`: Die Hälften sind **beschreibbar**, aber nicht auf einen Blick zuzuordnen („42“ und „6 · 7“). Die
  Kinder sagen sich ihre Karten vor.
- `bothAgree`: Die falschen Antworten sind **echte Denkfehler** (z. B. vertauschte Ziffern, falsche Wortart, falsche
  Einheit). Dann müssen die Kinder sich begründen.

Schlecht:
- Ein Hinweis, der nur die Antwort enthält („Die Antwort ist 48.“), und eine Frage, die man auch ohne Hinweis lösen kann.
  Dann tippt ein Kind allein.
- Die Frage steht ganz im Hinweis, die Zahl im anderen Text: Das Hinweis-Kind kann die Aufgabe selbst lösen und
  nur sagen „tipp 48“. Das Hinweis-Kind sollte **nur Daten** haben und die **Rechnung bleibt beim anderen**, oder umgekehrt.
- `matchPairs` mit Karten, die identisch aussehen oder zwei mögliche Partner haben (z. B. „4 · 5“ und „2 · 10“ zu „20“).
- `bothAgree` mit drei offensichtlich albernen Antworten. Dann klickt jeder allein die richtige.
- `relay`, bei dem Schritt 2 die Zahl aus Schritt 1 gar nicht braucht.
- Aufgaben, die nur Raten sind, oder deren Lösung außerhalb des Textes unklar ist.
- Mehrere richtige Antworten.
- Textwände. Kinder müssen vorlesen können: höchstens zwei, drei kurze Sätze pro Hinweis.

Weitere Hinweise:
- Wechselnde Formulierungen und Aufgabentypen in einem Level, nicht fünfmal dasselbe.
- Fehler dürfen **nicht** durch Raten leicht zu überspringen sein: Bei `bothAgree` mit nur 2 Antworten steht die Raten-
  Chance bei 50 Prozent je Kind.
- Immer erst selbst durchrechnen oder die Fakten prüfen; die Lösung steht im JSON, das Programm kennt keine Alternativen.
- Tonfall: freundlich, kurze Sätze, passend zum Alter. Keine Werbung, keine Marken, keine Namen echter Kinder.

## 16. Prüfen: Editor, Skript, App-Prüfer

### Editor (JSON Schema)
Das Schema `docs/schema/pack.schema.json` (JSON Schema Draft 2020-12) beschreibt `pack.json` so genau, wie es mit einem
Schema geht: Pflichtfelder, erlaubte Werte, ID-Muster, die Aufgabentypen und Visuals. Mit einem Hinweis am Anfang
der Datei prüfen Editoren wie Visual Studio Code beim Tippen:

```json
{
  "$schema": "../../docs/schema/pack.schema.json",
  "id": "de.familie-muster.kurse"
}
```

Der Pfad ist relativ zur `pack.json` (hier im Ordner `packs/<id>/`). Der Schlüssel `$schema` ist unschädlich: Die App
liest `pack.json` mit Swifts `JSONDecoder`, und der ignoriert unbekannte Schlüssel. Du musst ihn vor dem Einspielen nicht
entfernen.

Was das Schema **nicht** prüft: dass `level`/`requires`/`place` auf vorhandene Level und Orte zeigen, dass die Level-ID
mit der Paket-ID beginnt, dass Paar-Hälften eindeutig sind, ob `relay` glatt aufgeht, und die Bilddatei.

### Prüfskript
```
python3 tools/check_format.py packs/*/pack.json
```
Braucht nur Python 3. Prüft das Schema-Übliche plus Verweise zwischen Orten und Leveln, Fächer, Wege, Start, die
Bilddatei (vorhanden, Endung, höchstens 8 MB, Seitenlänge 512 bis 8192, stimmt mit `width`/`height` überein) und die
Aufgabenregeln. Es läuft bei jedem Pull Request automatisch.

### App-Prüfer
`huckepack-lint` aus dem (noch nicht öffentlichen) App-Repository nutzt dieselben Regeln wie die App selbst. Der
Betreuer führt ihn vor dem Zusammenführen aus.

## 17. Checkliste vor dem Einreichen

- [ ] Paket-ID hat mindestens drei Teile, Ordnername = Paket-ID, `version` erhöht.
- [ ] `title`, `author`, `licence` (`CC-BY-4.0`) gesetzt; `de` überall vorhanden.
- [ ] Alle Level-IDs beginnen mit `<Paket-ID>/`; `schemaVersion` fehlt oder ist 1; `grade` 1 bis 13.
- [ ] Jedes Level hat 4 bis 6 Aufgaben, davon mindestens 4 mit `difficulty` 1 oder 2.
- [ ] Jede Aufgabe braucht **beide** Kinder (siehe Abschnitt 15) und hat genau eine richtige Lösung.
- [ ] Alle Lösungen nachgerechnet, alle Fakten geprüft (auch `relay`: Schritt 2 stimmt mit der Operation überein).
- [ ] Antworten im richtigen Format: Cent bei `euroCents`, Minuten seit Mitternacht bei `time`, Minuten bei `minutes`.
- [ ] `relay.second` enthält `{x}` in jeder Sprache.
- [ ] Alle Fähigkeiten sind wohlgeformt und die neuen haben einen Namen in `skills`.
- [ ] Eigene Kurse stehen in `courses`.
- [ ] Welt-Paket: Bild liegt neben `pack.json`, Maße stimmen, höchstens 8 MB; `start`
      gesetzt; jeder Ort ist über Wege erreichbar; jedes Ortslevel hat kein `place`; jedes Band hat ein `place` eines
      Ortes mit eigenem Level.
- [ ] `python3 tools/check_format.py packs/*/pack.json` ist grün.
- [ ] Keine Aufgaben aus Schulbüchern oder Webseiten abgeschrieben; keine echten Namen von Kindern; keine Marken,
      Links oder Emojis.
