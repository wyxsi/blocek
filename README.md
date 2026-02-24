# Rozdelovac blockov

Aplikacia na rozdelenie nakupu z blocku medzi 2 ludi.

## Pouzitie

### Webova verzia (JavaScript)
1. Otvor https://wyxsi.github.io/blocek v prehliadaci
2. Nahraj PDF blocku
3. Polozky sa automaticky extrahuju
4. Prirad kazdu polozku:
   - Osoba 1
   - Osoba 2
   - Oba (rozdelit na polovicu)
   - Vylucit
5. Zobrazia sa 2 sumy

### Lokalne spustenie
Stiahni index.html a otvor v prehliadaci.

### Python verzia
```bash
pip install streamlit pdfplumber
streamlit run split_bill.py
```

## Podporovane obchody

- Kaufland
- Action
- Ine obchody s PDF blockmi

## Hosting

- **GitHub Pages**: Automaticky na https://wyxsi.github.io/blocek
- **Streamlit Cloud**: Pripoj repo na streamlit.io/cloud
