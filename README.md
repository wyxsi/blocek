# 🧾 Rozdeľovač bločkov

Aplikácia na rozdelenie nákupu z bločku medzi 2 ľudí.

## Použitie

### Webová verzia
1. Otvor [https://wyxsi.github.io/blocek/](https://wyxsi.github.io/blocek/) v prehliadači
2. Nahraj PDF bločku
3. Položky sa automaticky extrahujú
4. Prirad každú položku:
   - 👤 Osoba 1
   - 👤 Osoba 2
   - ½ Oba (rozdeliť na polovicu)
   - ❌ (vylúčiť)
5. Zobrazia sa 2 sumy

### Lokálne spustenie
Stiahni `index.html` a otvor v prehliadači.

### Python verzia (Streamlit)
```bash
pip install streamlit pdfplumber
streamlit run split_bill.py
```

## Podporované obchody

- Kaufland
- Action
- Iné obchody s PDF bločkami

## Hosting

- **GitHub Pages**: https://wyxsi.github.io/blocek/
- **Streamlit Cloud**: Pripoj repo na streamlit.io/cloud
