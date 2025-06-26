#!/usr/bin/env python3

import os, requests, json, time
from dotenv import load_dotenv

load_dotenv()
API_KEY_AVAIL = os.getenv("WHOISXMLAPI_KEY_AVAILABILITY")
API_KEY_WHOIS = os.getenv("WHOISXMLAPI_KEY_WHOIS")

def load_tlds(path="tlds.json"):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return {r["region"]: [d for d in r["domains"] if d["tld"].startswith(".")] for r in data}
    except: return {}

def check_avail(domain):
    if not API_KEY_AVAIL: return "ERR"
    try:
        r = requests.get(
            "https://domain-availability.whoisxmlapi.com/api/v1",
            params={"apiKey": API_KEY_AVAIL, "domainName": domain},
            timeout=10,
        ).json()
        s = r.get("DomainInfo", {}).get("domainAvailability", "UNKNOWN")
        return "AVAILABLE" if s == "AVAILABLE" else ("UNAVAILABLE" if s == "UNAVAILABLE" else "UNKNOWN")
    except: return "ERR"

def fmt(stat, dom, c=""):
    p = f"{dom} - ({c}) " if c else f"{dom} - "
    return p + {"AVAILABLE": "DOSTĘPNA ✅", "UNAVAILABLE": "ZAJĘTA ❌", "UNKNOWN": "NIEZNANA ❓", "ERR": "BŁĄD ⚠️"}[
        stat
    ]

def whois(domain):
    if not API_KEY_WHOIS: return "Brak klucza WHOIS"
    try:
        r = requests.get(
            "https://www.whoisxmlapi.com/whoisserver/WhoisService",
            params={"apiKey": API_KEY_WHOIS, "domainName": domain, "outputFormat": "JSON", "da": 2},
            timeout=15,
        ).json()
        rec, rd = r.get("WhoisRecord", {}), r.get("WhoisRecord", {}).get("registryData", {})
        return "\n".join(
            [
                f"--- WHOIS {domain} ---",
                f"Utworzenie: {rd.get('createdDate', 'N/A')}",
                f"Wygasa: {rd.get('expiresDate', 'N/A')}",
                f"Aktualizacja: {rd.get('updatedDate', 'N/A')}",
                f"Rejestrator: {rec.get('registrarName', 'N/A')}",
            ]
        )
    except Exception as e:
        return f"BŁĄD WHOIS: {e}"

def check_category(base, cat, tlds):
    print(f"\n--- {base} / {cat} ---\n")
    for d in tlds:
        dom = f"{base}{d['tld']}"
        print(fmt(check_avail(dom), dom, d.get("country", "")))
        time.sleep(0.6)
    print("--------------------------------------------------")

def menu():
    print(
        "\n======================================\n"
        " Sprawdzanie Domen WhoisXMLAPI\n"
        "======================================\n"
        "1. Pojedyncza domena\n"
        "2. Kategoria TLD\n"
        "3. WHOIS\n"
        "0. Wyjście\n"
        "--------------------------------------"
    )

def main():
    if not (API_KEY_AVAIL or API_KEY_WHOIS):
        print("Brak kluczy API"); return

    all_tlds = load_tlds()
    menu_keys = sorted(all_tlds.keys())

    base_cache = ""
    while True:
        menu()
        ch = input("Wybierz: ").strip()
        skip_pause = False

        if ch == "1":
            while True:
                d = input("\nDomena (0 powrót): ").strip()
                if d == "0": break
                if d: print(fmt(check_avail(d), d))
            skip_pause = True

        elif ch == "2":
            if not base_cache:
                base_cache = input("\nBazowa nazwa domeny: ").strip()
                if not base_cache: continue
            while True:
                print("\nKategorie:")
                for i, k in enumerate(menu_keys): print(f"  {chr(97+i)}. {k}")
                print("  z. Zmień nazwę bazową\n  0. Powrót")
                s = input("Opcja: ").strip().lower()
                if s == "0": break
                if s == "z": base_cache = ""; break
                idx = ord(s) - 97
                if 0 <= idx < len(menu_keys):
                    cat = menu_keys[idx]
                    check_category(base_cache, cat, all_tlds[cat])

        elif ch == "3":
            while True:
                d = input("\nDomena do WHOIS (0 powrót): ").strip()
                if d == "0": break
                if d: print(whois(d))
            skip_pause = True

        elif ch == "0":
            print("Do widzenia!"); break
        else:
            print("Zła opcja")

        if not skip_pause:
            input("\nEnter aby kontynuować...")
            os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()

