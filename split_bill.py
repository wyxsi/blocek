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
            if text:
                lines = text.split('\n')
                i = 0
                while i < len(lines) - 1:
                    current_line = lines[i].strip()
                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                    
                    if re.match(r'^\d+\.\d+%\s*\d+\.\d+€$', next_line) and current_line:
                        match = re.match(r'^\d+\.\d+%\s*(\d+\.\d+)€$', next_line)
                        if match:
                            price_str = match.group(1).replace('€', '').replace(',', '.').replace('-', '')
                            try:
                                price = float(price_str)
                                if price > 0:
                                    items.append({"name": current_line, "price": price})
                            except:
                                pass
                            i += 2
                            continue
                    i += 1
    return items

uploaded_file = st.file_uploader("Nahraj PDF bločku", type="pdf")

if uploaded_file:
    if st.button("Extrahovať položky z PDF"):
        st.session_state.extracted_items = extract_items_from_pdf(uploaded_file)
        st.session_state.assigned = {i: "none" for i in range(len(st.session_state.extracted_items))}
    
    if st.session_state.extracted_items:
        st.subheader(f"Nájdených {len(st.session_state.extracted_items)} položiek")
        
        for i, item in enumerate(st.session_state.extracted_items):
            col1, col2, col3, col4 = st.columns([3, 1, 2, 2])
            with col1:
                st.write(f"**{item['name']}**")
            with col2:
                st.write(f"{item['price']:.2f} €")
            with col3:
                options = ["❌", "👤 Osoba 1", "👤 Osoba 2", "½ Oba"]
                current_idx = ["none", "person1", "person2", "split"].index(st.session_state.assigned.get(i, "none"))
                choice = st.selectbox(f"Priradiť", options, index=current_idx, key=f"select_{i}", label_visibility="collapsed")
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
        
        st.info(f"Celkom: {sum(item['price'] for item in st.session_state.extracted_items):.2f} €")
