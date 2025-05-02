import streamlit as st
import pandas as pd
from address_utils import validate_addresses, find_similar_pairs
from data_utils import load_file, export_csv

st.set_page_config(page_title="US Address Similarity Checker", layout="wide")
st.title("🏠 US Address Similarity & Validation Report")

uploaded_file = st.file_uploader("Upload CSV or JSON file", type=["csv", "json"])

if uploaded_file:
    df = load_file(uploaded_file)
    st.write("✅ File loaded! Columns detected:")
    st.write(df.columns.tolist())

    address_column = st.selectbox("Select the address column", df.columns)
    display_count = st.selectbox("Select number of rows to display", [5, 10, 25, 50, 100], index=0)

    if st.button("Run Analysis"):
        valid_addresses, invalid_addresses = validate_addresses(df[address_column])
        threshold = st.slider("Set similarity threshold (%)", 70, 100, 85, 1)
        similar_pairs = find_similar_pairs(valid_addresses, threshold)
        deduped_valid = list(set(valid_addresses))

        st.success(f"✅ Total records: {len(df)}")
        st.success(f"✅ Valid addresses: {len(valid_addresses)}")
        st.warning(f"❌ Invalid/unparseable addresses: {len(invalid_addresses)}")
        st.info(f"🔍 Similar pairs found (>{threshold}%): {len(similar_pairs)}")

        # Display and download dataframes
        for name, data in [
            ("✅ Valid Addresses", valid_addresses),
            ("🔄 Deduplicated Valid Addresses", deduped_valid),
            ("❌ Invalid or Unparseable Addresses", invalid_addresses)
        ]:
            st.subheader(name)
            df_out = pd.DataFrame({name: data})
            st.dataframe(df_out.head(display_count))
            st.download_button(f"Download {name} (CSV)", export_csv(df_out), file_name=f"{name.replace(' ', '_').lower()}.csv", mime='text/csv')

        if similar_pairs:
            sim_df = pd.DataFrame(similar_pairs)
            st.subheader("🔍 Similar Address Pairs")
            st.dataframe(sim_df.head(display_count))
            st.download_button("Download Similar Address Pairs (CSV)", export_csv(sim_df), file_name="similar_address_pairs.csv", mime='text/csv')
        else:
            st.info("No similar address pairs found at the selected threshold.")
