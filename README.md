# AINUMPSA – SHADOW ENGINE

**Lustrzane odbicie głównego silnika rezonansu.**

> *0 < 1 – ale w cieniu też jest struktura.*

Shadow Engine to osobna gałąź projektu AINUMPSA.  
Przetwarza te same dane (NEO, tensory, geometrię), ale **odwraca ich wartości** – kolory, kąty, współczynniki, atraktory.

---

## Cel

- Generowanie wizualizacji dla serii NFT **SHADOW**
- Testowanie rezonansu w warunkach „negatywu”
- Rozszerzenie pola obserwacji o drugi biegun

---

## Portfel

`0x8e504ebd3f1eaa45df87d398b7cbcb823592b324`

---

## Struktura
AINUMPSA-Shadow-Engine/
├── README.md
├── src/
│ ├── init.py
│ ├── shadow_engine.py
│ ├── generate_assets.py
│ ├── time_travel.py
│ └── config.py
├── data/
│ └── shadow_neo_points.json
├── output/
│ └── assets/
└── .github/
└── workflows/
└── shadow_sync.yml

---

## Szybki start

```bash
# Instalacja zależności
pip install pillow opencv-python numpy

<br>

# Uruchomienie silnika
python src/shadow_engine.py

<br>

# Generowanie assetów
python src/generate_assets.py


───

Licencja
Wszelkie prawa zastrzeżone – do czasu podjęcia decyzji o otwarciu kodu.

───

1 > 0 – nawet w cieniu.
