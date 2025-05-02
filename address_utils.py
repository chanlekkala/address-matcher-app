import usaddress
from rapidfuzz import fuzz

def validate_addresses(address_series):
    valid_addresses = []
    invalid_addresses = []
    for addr in address_series.dropna().astype(str):
        try:
            parsed, _ = usaddress.tag(addr)
            if (all(k in parsed for k in ['AddressNumber', 'StreetName', 'PlaceName']) or
                all(k in parsed for k in ['USPSBoxType', 'USPSBoxID', 'PlaceName'])):
                valid_addresses.append(addr)
            else:
                invalid_addresses.append(addr)
        except:
            invalid_addresses.append(addr)
    return valid_addresses, invalid_addresses

def find_similar_pairs(valid_addresses, threshold):
    similar_pairs = []
    for i in range(len(valid_addresses)):
        for j in range(i + 1, len(valid_addresses)):
            try:
                parsed1, _ = usaddress.tag(valid_addresses[i])
                parsed2, _ = usaddress.tag(valid_addresses[j])

                if parsed1.get('AddressNumber') != parsed2.get('AddressNumber'):
                    continue
                if parsed1.get('OccupancyIdentifier') != parsed2.get('OccupancyIdentifier'):
                    continue

                comp1 = ' '.join([parsed1.get(k, '') for k in ['StreetName', 'StreetNamePostType', 'PlaceName', 'StateName', 'ZipCode']])
                comp2 = ' '.join([parsed2.get(k, '') for k in ['StreetName', 'StreetNamePostType', 'PlaceName', 'StateName', 'ZipCode']])

                score = fuzz.token_sort_ratio(comp1, comp2)
                if score >= threshold:
                    similar_pairs.append({'Address 1': valid_addresses[i], 'Address 2': valid_addresses[j], 'Similarity (%)': score})
            except:
                continue
    return similar_pairs
