import streamlit as st
import pdfplumber
import re

st.set_page_config(page_title="Rozdeľovač bločkov", page_icon="🧾")
st.title("🧾 Rozdeľovač bločkov")

if "extracted_items" not in st.session_state:
    st.session_state.extracted_items = []
if "assigned" not in st.session_state:
    st.session_state.assigned = {}

def extract_items_from_pdf(pdf_file):
    items = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            
            # Find lines with "X.XX ks * X.XX" or "X.XX ks * -X.XX" pattern
            qty_pattern = re.compile(r'^(\d+[.,]?\d*)\s*ks\s*\*\s*([+-]?\d+[.,]?\d*)$')
            
            seen = set()
            
            for i, line in enumerate(lines):
                match = qty_pattern.match(line.strip())
                if not match:
                    continue
                
                qty = float(match.group(1).replace(',', '.'))
                unit_price = float(match.group(2).replace(',', '.'))
                total_price = qty * unit_price
                
                if total_price == 0:
                    continue
                
                # Look back for product name
                name = None
                for j in range(i - 1, max(0, i - 6), -1):
                    check_line = lines[j].strip()
                    
                    # Skip if contains price or DPH
                    if '€' in check_line or '%' in check_line:
                        continue
                    # Skip quantity lines
                    if 'ks' in check_line or '*' in check_line:
                        continue
                    # Skip footer keywords
                    if any(kw in check_line for kw in ['SPOLU', 'NA ÚHRADU', 'DPH', 'Sadzba', 'Základ', 'Elektronická', 'Položky', 'Číslo dokladu']):
                        continue
                    # Skip short lines
                    if len(check_line) < 2:
                        continue
                    
                    name = check_line
                    break
                
                if not name:
                    continue
                
                key = f"{name}|{total_price:.2f}"
                if key in seen:
                    continue
                
                seen.add(key)
                items.append({"name": name, "price": total_price, "qty": qty})
    
    # Extract NA UHRADU total for comparison
    pdf_total = None
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        
        # Try different patterns
        match = re.search(r'NAÚHRADU\s*EUR?\s*(\d+[.,]?\d*)', text.replace(' ', ''))
        if match:
            pdf_total = float(match.group(1).replace(',', '.'))
        else:
            match = re.search(r'NA\s*ÚHRADU\s*EUR?\s*(\d+[.,]?\d*)', text)
            if match:
                pdf_total = float(match.group(1).replace(',', '.'))
    
    return items, pdf_total

uploaded_file = st.file_uploader("Nahraj PDF bločku", type="pdf")

if uploaded_file:
    if st.button("Extrahovať položky z PDF"):
        st.session_state.extracted_items, pdf_total = extract_items_from_pdf(uploaded_file)
        st.session_state.assigned = {i: "none" for i in range(len(st.session_state.extracted_items))}
        st.session_state.pdf_total = pdf_total
    
    if st.session_state.extracted_items:
        st.subheader(f"Nájdených {len(st.session_state.extracted_items)} položiek")
        
        for i, item in enumerate(st.session_state.extracted_items):
            col1, col2, col3 = st.columns([3, 1, 2])
            with col1:
                qty_str = f"({item['qty']}) " if item['qty'] > 1 else ""
                st.write(f"**{qty_str}{item['name']}**")
            with col2:
                st.write(f"{item['price']:.2f} €")
            with col3:
                options = ["❌", "👤 Osoba 1", "👤 Osoba 2", "½ Oba"]
                current_idx = ["none", "person1", "person2", "split"].index(st.session_state.assigned.get(i, "none"))
                choice = st.selectbox("Priradiť", options, index=current_idx, key=f"select_{i}", label_visibility="collapsed")
                st.session_state.assigned[i] = ["none", "person1", "person2", "split"][options.index(choice)]
        
        st.divider()
        
        total1 = sum(item["price"] if st.session_state.assigned[i] == "person1" else 0 for i, item in enumerate(st.session_state.extracted_items))
        total2 = sum(item["price"] if st.session_state.assigned[i] == "person2" else 0 for i, item in enumerate(st.session_state.extracted_items))
        split_total = sum(item["price"] / 2 if st.session_state.assigned[i] == "split" else 0 for i, item in enumerate(st.session_state.extracted_items))
        
        final1 = total1 + split_total
        final2 = total2 + split_total
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Osoba 1", f"{final1:.2f} €")
        with col2:
            st.metric("Osoba 2", f"{final2:.2f} €")
        
        # Total with comparison to PDF
        total = sum(item['price'] for item in st.session_state.extracted_items)
        total_text = f"Celkom: {total:.2f} €"
        
        if st.session_state.get('pdf_total'):
            diff = total - st.session_state.pdf_total
            if abs(diff) > 0.01:
                total_text += f" (PDF: {st.session_state.pdf_total:.2f} € - rozdiel: {diff:.2f} €)"
            else:
                total_text += " ✓"
        
        st.info(total_text)
