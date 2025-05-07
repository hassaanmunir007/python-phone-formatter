import streamlit as st
import pandas as pd
import re
from io import StringIO

def clean_phone_number(phone):
    digits = re.sub(r'\D', '', str(phone))
    if digits.startswith('1') and len(digits) == 11:
        return f'+{digits}'
    elif len(digits) == 10:
        return f'+1{digits}'
    elif digits.startswith('+') and len(digits) > 11:
        return digits
    return f'+{digits}'

st.title("Phone Number Formatter Tool")

uploaded_file = st.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Find 'phone number' column (case-insensitive)
    phone_col = next((col for col in df.columns if col.lower() == 'phone number'), None)
    if not phone_col:
        st.error("No 'phone number' column found in the uploaded CSV.")
    else:
        df['phone number formatted'] = df[phone_col].apply(clean_phone_number)

        st.success("Phone numbers formatted!")
        st.dataframe(df)

        # Allow download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Updated CSV",
            csv,
            "formatted_numbers.csv",
            "text/csv",
        )
