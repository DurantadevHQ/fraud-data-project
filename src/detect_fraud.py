◊◊# detect_fraud.py - Sample function to check domains against a blacklist
# For full implementation, see our enterprise API: https://durantadev.com

import pandas as pd

def load_blacklist(csv_path='data/blacklist.csv'):
    """Load the blacklist from the CSV file."""
    try:
        df = pd.read_csv(csv_path)
        return set(df['domain'].tolist())
    except FileNotFoundError:
        print("Blacklist file not found. Please ensure the path is correct.")
        return set()

def is_domain_blacklisted(domain, blacklist):
    """Check if a single domain is in the blacklist."""
    return domain in blacklist

# Example usage
if __name__ == "__main__":
    # Load the blacklist
    blacklist = load_blacklist()
    
    # Check some example domains
    test_domains = ['example.com', 'celebrity-gossip.online', 'google.com']
    
    for domain in test_domains:
        if is_domain_blacklisted(domain, blacklist):
            print(f"🚨 {domain} is blacklisted.")
        else:
            print(f"✅ {domain} is clean.")
