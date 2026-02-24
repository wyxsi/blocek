# 🧾 Rozdeľovač bločkov

Aplikácia na rozdelenie nákupu z bločku medzi 2 ľudí.

## Použitie

### Webová verzia
1. Stiahni `index.html` a otvor v prehliadači
2. Nahraj PDF bločku
3. Položky sa automaticky extrahujú
4. Prirad každú položku:
   - 👤 Osoba 1
   - 👤 Osoba 2
   - ½ Oba (rozdeliť na polovicu)
   - ❌ (vylúčiť)
5. Zobrazia sa 2 sumy

### Python verzia (Streamlit)
```bash
pip install streamlit pdfplumber
streamlit run split_bill.py
```

## Podporované obchody

- Kaufland
- Action
- Iné obchody s PDF bločkami
