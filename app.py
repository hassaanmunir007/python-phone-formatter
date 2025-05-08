import streamlit as st
import pandas as pd
import re
from io import StringIO, BytesIO

def clean_phone_number(phone):
    if not phone:
        return ''

    phone = str(phone).strip()
    
    # Remove everything except numbers
    digits_only = re.sub(r'\D', '', phone)

    # Normalize to +1XXXXXXXXXX format
    if digits_only.startswith('1') and len(digits_only) == 11:
        return f'+{digits_only}'
    elif len(digits_only) == 10:
        return f'+1{digits_only}'
    elif phone.startswith('+') and len(digits_only) > 10:
        return f'+{digits_only}'  # Retain original + if valid
    else:
        return f'+{digits_only}'


st.title("📞 Phone Number Formatter Tool (Batch CSVs)")

uploaded_files = st.file_uploader("Upload one or more CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"Processing: {file.name}")
        try:
            df = pd.read_csv(file)
            phone_col = next((col for col in df.columns if col.lower() == 'phone number'), None)

            if not phone_col:
                st.error(f"No 'phone number' column found in {file.name}")
                continue

            df['phone number formatted'] = df[phone_col].apply(clean_phone_number)
            st.success(f"{file.name} formatted successfully!")
            st.dataframe(df)

            csv_bytes = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"Download {file.name} (formatted)",
                data=csv_bytes,
                file_name=f"formatted_{file.name}",
                mime='text/csv'
            )
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")
