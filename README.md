# 🛡️ Ethereum Wallet Risk Scoring Tool

This project implements a Python-based tool to assess the **risk profile of Ethereum wallet addresses**. By leveraging the **Moralis API**, it fetches on-chain data and applies a comprehensive scoring model to assign a **risk score from 0 to 1000**, categorizing wallets from **Very Low Risk** to **Very High Risk**.

---

## ✨ Features

- 🔍 **Multi-Factor Risk Assessment**: Combines multiple on-chain metrics for a holistic risk profile.
- 🛑 **Spam Token Detection**: Detects scam tokens using Moralis flags and custom keyword matching.
- 📊 **Activity Analysis**: Evaluates transaction activity and wallet dormancy.
- 🕰️ **Wallet Age Calculation**: Scores based on how long a wallet has been active.
- 🧾 **Portfolio Diversity Check**: Assesses the variety of tokens held.
- 💰 **ETH Balance Evaluation**: Considers native ETH balance as a risk factor.
- 🎯 **0–1000 Risk Score**: Easy-to-interpret numeric risk scale.
- 🏷 **Risk Categorization**: Maps scores to qualitative labels like _"High Risk"_.
- 📤 **CSV & JSON Output**: Exports results for both overview and detailed review.
- ⏳ **Progress Tracking**: Displays real-time updates when analyzing multiple wallets.

---

## ⚙️ How It Works

### 1. 📥 Data Collection

The tool uses the **Moralis API (v2)** to fetch essential on-chain data from the Ethereum mainnet:

- **ERC-20 Token Balances**  
  Endpoint: `/{address}/erc20`  
  Retrieves tokens held, spam flags, names, and balances.

- **Transaction History**  
  Endpoint: `/{address}`  
  Determines total transactions, age, and last active timestamp.

- **ETH Balance**  
  Endpoint: `/{address}/balance`  
  Gets current native ETH holdings.

> ⏱️ A short delay is added between API calls to avoid rate limits, especially on free-tier usage.

---

### 2. 🧠 Feature Breakdown & Rationale

| Feature                | Description                                                                                  |
|------------------------|----------------------------------------------------------------------------------------------|
| **Spam Token Risk**     | Detects wallets with spammy tokens (e.g., "claim", "free", ".com") using Moralis spam flags |
| **Activity Risk**       | Considers tx count and dormancy to identify abandoned or burner wallets                     |
| **Wallet Age Risk**     | Scores higher risk for wallets less than 30 days old                                        |
| **Portfolio Diversity** | Checks number of distinct ERC-20 tokens (too few or too many is risky)                      |
| **Native Balance Risk** | Evaluates if wallet has sufficient ETH for normal use                                       |

---

## 🧮 Risk Scoring Methodology

### 🔢 Individual Scores (0–100)

Each of the five factors is independently scored. A **higher score** means **higher risk**.

### ⚖️ Weighted Average

| Feature               | Weight |
|------------------------|--------|
| Spam Token Risk        | 30%    |
| Activity Risk          | 25%    |
| Wallet Age Risk        | 20%    |
| Portfolio Diversity    | 15%    |
| Native Balance Risk    | 10%    |

**Composite Score (0–100)**:
Composite_Score = (Spam × 0.30) + (Activity × 0.25) + (Age × 0.20) + (Diversity × 0.15) + (Balance × 0.10)

### 🎯 Final Score (0–1000)
Final_Score = Composite_Score × 10

---

## 🏷 Risk Categories

| Category         | Score Range |
|------------------|-------------|
| 🔴 VERY HIGH RISK | ≥ 750       |
| 🟠 HIGH RISK      | ≥ 550       |
| 🟡 MEDIUM RISK    | ≥ 350       |
| 🟢 LOW RISK       | ≥ 200       |
| ✅ VERY LOW RISK  | < 200       |

---

## 📁 Output Files

After execution, the script generates:

### ✅ `wallet_risk_analysis_YYYYMMDD_HHMMSS.csv`

A concise CSV with each wallet’s risk score.
wallet_id,risk_score
0xfaa0768bde629806739c3a4620656c5d26f44ef2 , 732

### ✅ `wallet_risk_analysis_YYYYMMDD_HHMMSS.json`

A detailed JSON per wallet including:
- Raw API data
- All calculated risk metrics
- Composite and final score
- Risk category
