# 🧾 Rozdeľovač bločkov

Aplikácia na rozdelenie nákupu z bločku medzi 2 ľudí.

## Použitie

### JavaScript verzia (index.html)
1. Otvor `index.html` v prehliadači
2. Nahraj PDF bločku
3. Prirad každú položku:
   - 👤 Osoba 1
   - 👤 Osoba 2
   - ½ Oba (rozdeliť na polovicu)
   - ❌ (vylúčiť)
4. Zobrazia sa 2 sumy

### Python verzia (split_bill.py)
```bash
pip install streamlit pdfplumber
streamlit run split_bill.py
```

## Hosting

- **Streamlit Cloud**: Pripoj GitHub repo na streamlit.io/cloud
- **Vlastný server**: Spusti Python verziu na VPS
- **GitHub Pages**: JavaScript verzia funguje priamo v prehliadači
