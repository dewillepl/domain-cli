```markdown
# Domain CLI – sprawdzanie dostępności domen i WHOIS

Terminalowa aplikacja Pythona, która:
* sprawdza dostępność pojedynczych domen,
* sprawdza hurtowo nazwy w wybranych kategoriach TLD (ładowanych z `tlds.json`),
* pobiera dane WHOIS,
* działa w pętli – bez ciągłego restartu.

> Silnik korzysta z API [WhoisXMLAPI](https://www.whoisxmlapi.com/).

---

## Wymagania

* Python ≥ 3.9
* Konto w WhoisXMLAPI + 2 klucze:
  * `WHOISXMLAPI_KEY_AVAILABILITY`
  * `WHOISXMLAPI_KEY_WHOIS`

## Instalacja

```bash
git clone https://github.com/USER/REPO.git
cd REPO
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Minimalny `requirements.txt`:

```
requests
python-dotenv
```

## Konfiguracja

1. Utwórz plik `.env`:

```
WHOISXMLAPI_KEY_AVAILABILITY=TWÓJ_KLUCZ_1
WHOISXMLAPI_KEY_WHOIS=TWÓJ_KLUCZ_2
```

2. Upewnij się, że w katalogu znajduje się `tlds.json`
   (przykład poniżej – możesz dodać dowolne regiony).

```json
[
  {
    "region": "popularne",
    "domains": [
      { "country": "Commercial", "tld": ".com" },
      { "country": "Poland",     "tld": ".pl",   "iso2": "PL" }
    ]
  },
  {
    "region": "europa",
    "domains": [
      { "country": "Germany", "tld": ".de", "iso2": "DE" },
      { "country": "France",  "tld": ".fr", "iso2": "FR" }
    ]
  }
]
```

## Uruchomienie

```bash
python app.py
```

Po starcie zobaczysz menu:

```
1. Pojedyncza domena
2. Kategoria TLD
3. WHOIS
0. Wyjście
```

Sterowanie odbywa się poprzez wpisywanie opcji oraz nazw domen.

### Przykłady

• Dostępność pojedynczej domeny
```
Domena (0 powrót): example.ai
example.ai - DOSTĘPNA ✅
```

• Sprawdzenie „example” w regionie „europa”
```
--- example / europa ---

example.de - (Germany) - ZAJĘTA ❌
example.fr - (France)  - DOSTĘPNA ✅
--------------------------------------------------
```

• WHOIS
```
--- WHOIS example.com ---
Utworzenie: 1995-08-13T04:00:00Z
Wygasa:     2025-08-12T04:00:00Z
Aktualizacja:2023-07-10T09:14:25Z
Rejestrator: Example Registrar LLC
```

## Struktura

```
app.py         # główny skrypt
tlds.json      # lista regionów i TLD
.env           # klucze API
requirements.txt
README.md
```

## Licencja

MIT
```
