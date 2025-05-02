import streamlit as st
import pandas as pd
import usaddress
from rapidfuzz import fuzz

st.set_page_config(page_title="US Address Similarity Checker", layout="wide")
st.title("🏠 US Address Similarity & Validation Report")

uploaded_file = st.file_uploader("Upload CSV or JSON file", type=["csv", "json"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_json(uploaded_file)

    st.write("✅ File loaded! Columns detected:")
    st.write(df.columns.tolist())

    address_column = st.selectbox("Select the address column", df.columns)
    display_count = st.selectbox("Select number of rows to display", [5, 10, 25, 50, 100], index=0)

    if st.button("Run Analysis"):
        addresses = df[address_column].dropna().astype(str).tolist()

        valid_addresses = []
        invalid_addresses = []

        for addr in addresses:
            try:
                parsed, _ = usaddress.tag(addr)
                if all(k in parsed for k in ['AddressNumber', 'StreetName', 'PlaceName']):
                    valid_addresses.append(addr)
                else:
                    invalid_addresses.append(addr)
            except:
                invalid_addresses.append(addr)

        threshold = st.slider("Set similarity threshold (%)", 70, 100, 85, 1)
        similar_pairs = []

        for i in range(len(valid_addresses)):
            for j in range(i + 1, len(valid_addresses)):
                try:
                    parsed1, _ = usaddress.tag(valid_addresses[i])
                    parsed2, _ = usaddress.tag(valid_addresses[j])

                    # Check house number
                    if parsed1.get('AddressNumber') != parsed2.get('AddressNumber'):
                        continue

                    # Check unit (if present)
                    if parsed1.get('OccupancyIdentifier') != parsed2.get('OccupancyIdentifier'):
                        continue

                    # Build comparable strings (without house/unit)
                    components1 = ' '.join([
                        parsed1.get('StreetName', ''),
                        parsed1.get('StreetNamePostType', ''),
                        parsed1.get('PlaceName', ''),
                        parsed1.get('StateName', ''),
                        parsed1.get('ZipCode', '')
                    ])

                    components2 = ' '.join([
                        parsed2.get('StreetName', ''),
                        parsed2.get('StreetNamePostType', ''),
                        parsed2.get('PlaceName', ''),
                        parsed2.get('StateName', ''),
                        parsed2.get('ZipCode', '')
                    ])

                    score = fuzz.token_sort_ratio(components1, components2)

                    if score >= threshold:
                        similar_pairs.append({
                            'Address 1': valid_addresses[i],
                            'Address 2': valid_addresses[j],
                            'Similarity (%)': score
                        })
                except:
                    continue

        deduped_valid = list(set(valid_addresses))

        st.success(f"✅ Total records: {len(df)}")
        st.success(f"✅ Valid addresses: {len(valid_addresses)}")
        st.warning(f"❌ Invalid/unparseable addresses: {len(invalid_addresses)}")
        st.info(f"🔍 Similar pairs found (>{threshold}%): {len(similar_pairs)}")

        # Valid addresses
        st.subheader("✅ Valid Addresses")
        valid_df = pd.DataFrame({'Valid Address': valid_addresses})
        st.dataframe(valid_df.head(display_count))
        csv_valid = valid_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download All Valid Addresses (CSV)",
            data=csv_valid,
            file_name='valid_addresses.csv',
            mime='text/csv',
        )

        # Deduplicated addresses
        st.subheader("🔄 Deduplicated Valid Addresses")
        dedup_df = pd.DataFrame({'Deduplicated Address': deduped_valid})
        st.dataframe(dedup_df.head(display_count))
        csv_dedup = dedup_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Deduplicated Valid Addresses (CSV)",
            data=csv_dedup,
            file_name='deduplicated_valid_addresses.csv',
            mime='text/csv',
        )

        # Invalid addresses
        st.subheader("❌ Invalid or Unparseable Addresses")
        invalid_df = pd.DataFrame({'Invalid Address': invalid_addresses})
        st.dataframe(invalid_df.head(display_count))
        csv_invalid = invalid_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Invalid Addresses (CSV)",
            data=csv_invalid,
            file_name='invalid_addresses.csv',
            mime='text/csv',
        )

        # Similar pairs
        st.subheader("🔍 Similar Address Pairs")
        if similar_pairs:
            sim_df = pd.DataFrame(similar_pairs)
            st.dataframe(sim_df.head(display_count))
            csv_sim = sim_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Similar Address Pairs (CSV)",
                data=csv_sim,
                file_name='similar_address_pairs.csv',
                mime='text/csv',
            )
        else:
            st.info("No similar address pairs found at the selected threshold.")
