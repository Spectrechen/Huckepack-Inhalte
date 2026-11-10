`check_format.py` prüft das Format der Pakete (Level-Pakete und Welt-Pakete; läuft bei jedem Pull Request), nur mit
Python 3 und ohne weitere Pakete: `python3 tools/check_format.py packs/*/pack.json`. Bei Welt-Paketen prüft es auch die
Karte (Datei neben `pack.json`, Maße, Größe) und die Verweise zwischen Orten, Wegen und Leveln. Die vollständige Prüfung
mit den Regeln der App macht `huckepack-lint` aus dem (nicht öffentlichen) App-Repository; `--index` erzeugt den
Katalog-Index. Das Schema für Editoren liegt in `docs/schema/pack.schema.json`.
