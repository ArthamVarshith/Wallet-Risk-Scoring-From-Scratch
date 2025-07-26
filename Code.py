import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time


# Your Moralis API Key
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjU3NDUyNTI3LTZiZDEtNDE2OS1hN2I0LTgyNGE1MjAxMWM5NiIsIm9yZ0lkIjoiNDYxNjE0IiwidXNlcklkIjoiNDc0OTA5IiwidHlwZUlkIjoiMDFmODA3NGYtMzExMi00ZTQ0LTg2ZmItYzViZDkxZTNlNWVkIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NTM1NTM1MTIsImV4cCI6NDkwOTMxMzUxMn0.E6JKUdCeCWxMjIGNXqVbrmRd00znlAMSJ9FJ1-gzHn8"


# CORRECT BASE_URL (confirmed working)
BASE_URL = "https://deep-index.moralis.io/api/v2"


headers = {
    "Accept": "application/json",
    "X-API-Key": API_KEY
}


# Your 100 wallet addresses
WALLETS = [
    "0x0039f22efb07a647557c7c5d17854cfd6d489ef3",
    "0x06b51c6882b27cb05e712185531c1f74996dd988",
    "0x0795732aacc448030ef374374eaae57d2965c16c",
    "0x0aaa79f1a86bc8136cd0d1ca0d51964f4e3766f9",
    "0x0fe383e5abc200055a7f391f94a5f5d1f844b9ae",
    "0x104ae61d8d487ad689969a17807ddc338b445416",
    "0x111c7208a7e2af345d36b6d4aace8740d61a3078",
    "0x124853fecb522c57d9bd5c21231058696ca6d596",
    "0x13b1c8b0e696aff8b4fee742119b549b605f3cbc",
    "0x1656f1886c5ab634ac19568cd571bc72f385fdf7",
    "0x1724e16cb8d0e2aa4d08035bc6b5c56b680a3b22",
    "0x19df3e87f73c4aaf4809295561465b993e102668",
    "0x1ab2ccad4fc97c9968ea87d4435326715be32872",
    "0x1c1b30ca93ef57452d53885d97a74f61daf2bf4f",
    "0x1e43dacdcf863676a6bec8f7d6896d6252fac669",
    "0x22d7510588d90ed5a87e0f838391aaafa707c34b",
    "0x24b3460622d835c56d9a4fe352966b9bdc6c20af",
    "0x26750f1f4277221bdb5f6991473c6ece8c821f9d",
    "0x27f72a000d8e9f324583f3a3491ea66998275b28",
    "0x2844658bf341db96aa247259824f42025e3bcec2",
    "0x2a2fde3e1beb508fcf7c137a1d5965f13a17825e",
    "0x330513970efd9e8dd606275fb4c50378989b3204",
    "0x3361bea43c2f5f963f81ac70f64e6fba1f1d2a97",
    "0x3867d222ba91236ad4d12c31056626f9e798629c",
    "0x3a44be4581137019f83021eeee72b7dc57756069",
    "0x3e69ad05716bdc834db72c4d6d44439a7c8a902b",
    "0x427f2ac5fdf4245e027d767e7c3ac272a1f40a65",
    "0x4814be124d7fe3b240eb46061f7ddfab468fe122",
    "0x4839e666e2baf12a51bf004392b35972eeddeabf",
    "0x4c4d05fe859279c91b074429b5fc451182cec745",
    "0x4d997c89bc659a3e8452038a8101161e7e7e53a7",
    "0x4db0a72edb5ea6c55df929f76e7d5bb14e389860",
    "0x4e61251336c32e4fe6bfd5fab014846599321389",
    "0x4e6e724f4163b24ffc7ffe662b5f6815b18b4210",
    "0x507b6c0d950702f066a9a1bd5e85206f87b065ba",
    "0x54e19653be9d4143b08994906be0e27555e8834d",
    "0x56ba823641bfc317afc8459bf27feed6eb9ff59f",
    "0x56cc2bffcb3f86a30c492f9d1a671a1f744d1d2f",
    "0x578cea5f899b0dfbf05c7fbcfda1a644b2a47787",
    "0x58c2a9099a03750e9842d3e9a7780cdd6aa70b86",
    "0x58d68d4bcf9725e40353379cec92b90332561683",
    "0x5e324b4a564512ea7c93088dba2f8c1bf046a3eb",
    "0x612a3500559be7be7703de6dc397afb541a16f7f",
    "0x623af911f493747c216ad389c7805a37019c662d",
    "0x6a2752a534faacaaa153bffbb973dd84e0e5497b",
    "0x6d69ca3711e504658977367e13c300ab198379f1",
    "0x6e355417f7f56e7927d1cd971f0b5a1e6d538487",
    "0x70c1864282599a762c674dd9d567b37e13bce755",
    "0x70d8e4ab175dfe0eab4e9a7f33e0a2d19f44001e",
    "0x7399dbeebe2f88bc6ac4e3fd7ddb836a4bce322f",
    "0x767055590c73b7d2aaa6219da13807c493f91a20",
    "0x7851bdfb64bbecfb40c030d722a1f147dff5db6a",
    "0x7b4636320daa0bc055368a4f9b9d01bd8ac51877",
    "0x7b57dbe2f2e4912a29754ff3e412ed9507fd8957",
    "0x7be3dfb5b6fcbae542ea85e76cc19916a20f6c1e",
    "0x7de76a449cf60ea3e111ff18b28e516d89532152",
    "0x7e3eab408b9c76a13305ef34606f17c16f7b33cc",
    "0x7f5e6a28afc9fb0aaf4259d4ff69991b88ebea47",
    "0x83ea74c67d393c6894c34c464657bda2183a2f1a",
    "0x8441fecef5cc6f697be2c4fc4a36feacede8df67",
    "0x854a873b8f9bfac36a5eb9c648e285a095a7478d",
    "0x8587d9f794f06d976c2ec1cfd523983b856f5ca9",
    "0x880a0af12da55df1197f41697c1a1b61670ed410",
    "0x8aaece100580b749a20f8ce30338c4e0770b65ed",
    "0x8be38ea2b22b706aef313c2de81f7d179024dd30",
    "0x8d900f213db5205c529aaba5d10e71a0ed2646db",
    "0x91919344c1dad09772d19ad8ad4f1bcd29c51f27",
    "0x93f0891bf71d8abed78e0de0885bd26355bb8b1d",
    "0x96479b087cb8f236a5e2dcbfc50ce63b2f421da6",
    "0x96bb4447a02b95f1d1e85374cffd565eb22ed2f8",
    "0x9a363adc5d382c04d36b09158286328f75672098",
    "0x9ad1331c5b6c5a641acffb32719c66a80c6e1a17",
    "0x9ba0d85f71e145ccf15225e59631e5a883d5d74a",
    "0x9e6ec4e98793970a1307262ba68d37594e58cd78",
    "0xa7e94d933eb0c439dda357f61244a485246e97b8",
    "0xa7f3c74f0255796fd5d3ddcf88db769f7a6bf46a",
    "0xa98dc64bb42575efec7d1e4560c029231ce5da51",
    "0xb271ff7090b39028eb6e711c3f89a3453d5861ee",
    "0xb475576594ae44e1f75f534f993cbb7673e4c8b6",
    "0xb57297c5d02def954794e593db93d0a302e43e5c",
    "0xbd4a00764217c13a246f86db58d74541a0c3972a",
    "0xc179d55f7e00e789915760f7d260a1bf6285278b",
    "0xc22b8e78394ce52e0034609a67ae3c959daa84bc",
    "0xcbbd9fe837a14258286bbf2e182cbc4e4518c5a3",
    "0xcecf5163bb057c1aff4963d9b9a7d2f0bf591710",
    "0xcf0033bf27804640e5339e06443e208db5870dd2",
    "0xd0df53e296c1e3115fccc3d7cdf4ba495e593b56",
    "0xd1a3888fd8f490367c6104e10b4154427c02dd9c",
    "0xd334d18fa6bada9a10f361bae42a019ce88a3c33",
    "0xd9d3930ffa343f5a0eec7606d045d0843d3a02b4",
    "0xdde73df7bd4d704a89ad8421402701b3a460c6e9",
    "0xde92d70253604fd8c5998c8ee3ed282a41b33b7f",
    "0xded1f838ae6aa5fcd0f13481b37ee88e5bdccb3d",
    "0xebb8629e8a3ec86cf90cb7600264415640834483",
    "0xeded1c8c0a0c532195b8432153f3bfa81dba2a90",
    "0xf10fd8921019615a856c1e95c7cd3632de34edc4",
    "0xf340b9f2098f80b86fbc5ede586c319473aa11f3",
    "0xf54f36bca969800fd7d63a68029561309938c09b",
    "0xf60304b534f74977e159b2e159e135475c245526",
    "0xf67e8e5805835465f7eba988259db882ab726800",
    "0xf7aa5d0752cfcd41b0a5945867d619a80c405e52",
    "0xf80a8b9cfff0febf49914c269fb8aead4a22f847",
    "0xfe5a05c0f8b24fca15a7306f6a4ebb7dcf2186ac"
]


def get_wallet_tokens(address):
    """Get all token balances for a wallet"""
    url = f"{BASE_URL}/{address}/erc20"
    params = {"chain": "eth", "limit": 100, "exclude_spam": "false"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching tokens for {address}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception fetching tokens for {address}: {e}")
        return None


def get_wallet_transactions(address, limit=100):
    """Get transaction history for a wallet"""
    url = f"{BASE_URL}/{address}"
    params = {"chain": "eth", "limit": limit}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching transactions for {address}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception fetching transactions for {address}: {e}")
        return None


def get_native_balance(address):
    """Get ETH balance"""
    url = f"{BASE_URL}/{address}/balance"
    params = {"chain": "eth"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception:
        return None


def detect_spam_tokens(tokens):
    """Enhanced spam detection using both keywords and Moralis flags"""
    if not tokens:
        return 0, 0, []
    
    spam_keywords = [
        'visit', 'claim', 'reward', 'bonus', 'free', 'airdrop',
        '.com', '.org', '.net', 'http', 'www', '$', 'voucher',
        'gift', 'prize', 'winner', 'congratulations', 'eth', 'btc',
        'usd', '100x', 'moon', 'safe', 'doge', 'baby', 'mini'
    ]
    
    spam_count = 0
    total_tokens = len(tokens)
    spam_details = []
    
    for token in tokens:
        is_spam = False
        spam_reasons = []
        
        # Check Moralis built-in spam detection
        if token.get('possible_spam', False):
            is_spam = True
            spam_reasons.append('moralis_flagged')
        
        # Check keywords
        token_name = token.get('name', '').lower()
        token_symbol = token.get('symbol', '').lower()
        
        for keyword in spam_keywords:
            if keyword in token_name or keyword in token_symbol:
                is_spam = True
                spam_reasons.append(f'keyword_{keyword}')
                break
        
        # Check suspicious patterns
        if len(token_symbol) > 15 or any(char in token_name for char in ['$', '@', '#']):
            is_spam = True
            spam_reasons.append('suspicious_pattern')
        
        if is_spam:
            spam_count += 1
            spam_details.append({
                'name': token.get('name'),
                'symbol': token.get('symbol'),
                'address': token.get('token_address'),
                'reasons': spam_reasons
            })
    
    return spam_count, total_tokens, spam_details


def calculate_wallet_age_risk(transactions):
    """Calculate age-based risk"""
    if not transactions or not transactions.get('result'):
        return 50  # Unknown age = moderate risk
    
    txs = transactions['result']
    if not txs:
        return 50
    
    try:
        # Get oldest transaction (usually last in the list)
        oldest_tx = txs[-1] if len(txs) > 0 else txs[0]
        first_tx_date = datetime.fromisoformat(oldest_tx['block_timestamp'].replace('Z', '+00:00'))
        wallet_age_days = (datetime.now().replace(tzinfo=first_tx_date.tzinfo) - first_tx_date).days
        
        # Age-based risk scoring
        if wallet_age_days < 30:
            return 80  # Very new wallet = high risk
        elif wallet_age_days < 90:
            return 60  # New wallet = medium-high risk
        elif wallet_age_days < 365:
            return 30  # Moderate age = low-medium risk
        else:
            return 10  # Old wallet = low risk
            
    except Exception as e:
        print(f"Error calculating age risk: {e}")
        return 50


def calculate_wallet_risk_score(address):
    """Calculate comprehensive risk score for a wallet"""
    print(f"Analyzing wallet: {address}")
    
    # Get wallet data
    tokens = get_wallet_tokens(address)
    transactions = get_wallet_transactions(address)
    native_balance = get_native_balance(address)
    
    # Wait to avoid rate limiting
    time.sleep(0.25)
    
    risk_factors = {
        'address': address,
        'spam_risk': 0,
        'activity_risk': 0,
        'age_risk': 0,
        'diversity_risk': 0,
        'balance_risk': 0
    }
    
    # Risk Factor 1: Enhanced Spam Token Detection
    if tokens and 'result' in tokens:
        spam_count, total_tokens, spam_details = detect_spam_tokens(tokens['result'])
        
        if total_tokens > 0:
            spam_percentage = (spam_count / total_tokens) * 100
            if spam_percentage >= 80:
                risk_factors['spam_risk'] = 100
            elif spam_percentage >= 60:
                risk_factors['spam_risk'] = 85
            elif spam_percentage >= 40:
                risk_factors['spam_risk'] = 70
            elif spam_percentage >= 20:
                risk_factors['spam_risk'] = 50
            elif spam_count > 0:
                risk_factors['spam_risk'] = 25
        else:
            risk_factors['spam_risk'] = 30
        
        risk_factors['spam_tokens_count'] = spam_count
        risk_factors['total_tokens'] = total_tokens
        risk_factors['spam_percentage'] = round(spam_percentage, 1) if total_tokens > 0 else 0
        risk_factors['spam_details'] = spam_details[:5]  # Only store first 5 for space
    else:
        risk_factors['spam_tokens_count'] = 0
        risk_factors['total_tokens'] = 0
        risk_factors['spam_percentage'] = 0
        risk_factors['spam_risk'] = 40
    
    # Risk Factor 2: Activity Analysis
    if transactions and transactions.get('result'):
        tx_count = len(transactions['result'])
        risk_factors['transaction_count'] = tx_count
        
        if tx_count == 0:
            risk_factors['activity_risk'] = 100
        elif tx_count < 5:
            risk_factors['activity_risk'] = 90
        elif tx_count < 20:
            risk_factors['activity_risk'] = 70
        elif tx_count < 100:
            risk_factors['activity_risk'] = 40
        else:
            risk_factors['activity_risk'] = 10
        
        # Check last transaction date
        if tx_count > 0:
            try:
                last_tx = transactions['result'][0]
                last_tx_date = datetime.fromisoformat(last_tx['block_timestamp'].replace('Z', '+00:00'))
                days_since_last = (datetime.now().replace(tzinfo=last_tx_date.tzinfo) - last_tx_date).days
                
                # Add dormancy penalty
                if days_since_last > 730:  # 2 years
                    risk_factors['activity_risk'] = min(100, risk_factors['activity_risk'] + 40)
                elif days_since_last > 365:  # 1 year
                    risk_factors['activity_risk'] = min(100, risk_factors['activity_risk'] + 25)
                elif days_since_last > 180:  # 6 months
                    risk_factors['activity_risk'] = min(100, risk_factors['activity_risk'] + 15)
                
                risk_factors['days_since_last_tx'] = days_since_last
                risk_factors['last_transaction'] = last_tx_date.strftime('%Y-%m-%d')
            except Exception:
                risk_factors['days_since_last_tx'] = 9999
        else:
            risk_factors['days_since_last_tx'] = 9999
    else:
        risk_factors['transaction_count'] = 0
        risk_factors['activity_risk'] = 100
        risk_factors['days_since_last_tx'] = 9999
    
    # Risk Factor 3: Age Risk Calculation
    risk_factors['age_risk'] = calculate_wallet_age_risk(transactions)
    
    # Risk Factor 4: Portfolio Diversity
    if tokens and 'result' in tokens:
        token_count = len(tokens['result'])
        if token_count == 0:
            risk_factors['diversity_risk'] = 70
        elif token_count == 1:
            risk_factors['diversity_risk'] = 60
        elif token_count < 5:
            risk_factors['diversity_risk'] = 40
        elif token_count < 15:
            risk_factors['diversity_risk'] = 20
        elif token_count < 50:
            risk_factors['diversity_risk'] = 10
        else:
            # Too many tokens might indicate airdrop farming
            risk_factors['diversity_risk'] = min(30, token_count // 20)
    else:
        risk_factors['diversity_risk'] = 70
    
    # Risk Factor 5: Balance Risk
    if native_balance:
        balance_wei = int(native_balance.get('balance', '0'))
        balance_eth = balance_wei / 1e18
        
        if balance_eth == 0:
            risk_factors['balance_risk'] = 60
        elif balance_eth < 0.01:
            risk_factors['balance_risk'] = 40
        elif balance_eth < 0.1:
            risk_factors['balance_risk'] = 20
        else:
            risk_factors['balance_risk'] = 5
        
        risk_factors['eth_balance'] = round(balance_eth, 4)
    else:
        risk_factors['balance_risk'] = 50
        risk_factors['eth_balance'] = None
    
    # Calculate Composite Risk Score (0-100 scale)
    weights = {
        'spam_risk': 0.30,       # 30% - Spam detection
        'activity_risk': 0.25,   # 25% - Activity patterns  
        'age_risk': 0.20,        # 20% - Account age
        'diversity_risk': 0.15,  # 15% - Portfolio diversity
        'balance_risk': 0.10     # 10% - ETH balance
    }
    
    composite_score_100 = (
        risk_factors['spam_risk'] * weights['spam_risk'] +
        risk_factors['activity_risk'] * weights['activity_risk'] +
        risk_factors['age_risk'] * weights['age_risk'] +
        risk_factors['diversity_risk'] * weights['diversity_risk'] +
        risk_factors['balance_risk'] * weights['balance_risk']
    )
    
    # Normalize to 0-1000 scale
    composite_score_1000 = round(composite_score_100 * 10, 1)
    
    risk_factors['composite_risk_score'] = composite_score_1000
    
    # Risk Categories (adjusted for 0-1000 scale)
    if composite_score_1000 >= 750:
        risk_factors['risk_category'] = 'VERY HIGH RISK'
    elif composite_score_1000 >= 550:
        risk_factors['risk_category'] = 'HIGH RISK'
    elif composite_score_1000 >= 350:
        risk_factors['risk_category'] = 'MEDIUM RISK'
    elif composite_score_1000 >= 200:
        risk_factors['risk_category'] = 'LOW RISK'
    else:
        risk_factors['risk_category'] = 'VERY LOW RISK'
    
    # Display progress
    print(f"Risk: {risk_factors['composite_risk_score']}/1000 ({risk_factors['risk_category']})")
    print(f"Spam: {risk_factors['spam_tokens_count']}/{risk_factors['total_tokens']} ({risk_factors['spam_percentage']}%)")
    print(f"Transactions: {risk_factors['transaction_count']}, ETH: {risk_factors['eth_balance']}")
    
    return risk_factors


def analyze_all_wallets():
    """Analyze all wallets and generate comprehensive risk report"""
    results = []
    
    print(f"Starting analysis of {len(WALLETS)} wallets...")
    print("=" * 80)
    
    for i, wallet in enumerate(WALLETS):
        print(f"\n[{i+1}/{len(WALLETS)}] Processing: {wallet}")
        
        try:
            risk_data = calculate_wallet_risk_score(wallet)
            results.append(risk_data)
            
        except Exception as e:
            print(f"Error processing {wallet}: {e}")
            # Add error entry
            results.append({
                'address': wallet,
                'composite_risk_score': 1000, # Max risk for error
                'risk_category': 'ERROR - VERY HIGH RISK',
                'error': str(e)
            })
        
        # Rate limiting for free tier
        time.sleep(0.2)
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Sort by risk score (highest first)
    df = df.sort_values('composite_risk_score', ascending=False)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f'wallet_risk_analysis_{timestamp}.csv'
    json_filename = f'wallet_risk_analysis_{timestamp}.json'
    
    # Create the deliverable CSV: wallet_id, score
    deliverable_df = df[['address', 'composite_risk_score']].rename(columns={'address': 'wallet_id', 'composite_risk_score': 'score'})
    deliverable_df.to_csv(csv_filename, index=False)
    
    # Save detailed JSON
    with open(json_filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Display comprehensive summary
    print("\n" + "="*80)
    print("COMPREHENSIVE WALLET RISK ANALYSIS COMPLETE")
    print("="*80)
    
    print(f"\nRISK DISTRIBUTION:")
    risk_counts = df['risk_category'].value_counts()
    for category, count in risk_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {category}: {count} wallets ({percentage:.1f}%)")
    
    print(f"\nTOP 10 HIGHEST RISK WALLETS:")
    top_risk_cols = ['address', 'composite_risk_score', 'risk_category', 'spam_tokens_count', 'total_tokens', 'spam_percentage']
    print(df[top_risk_cols].head(10).to_string(index=False))
    
    print(f"\nFILES SAVED:")
    print(f"{csv_filename}")
    print(f"{json_filename}")
    
    return df


# Run the complete analysis
if __name__ == "__main__":
    print("MORALIS WALLET RISK ANALYSIS")
    print("Using confirmed working API endpoint")
    print("="*50)
    
    results_df = analyze_all_wallets()
    
    print(f"\nAnalysis complete! Check the CSV file for detailed results.")
