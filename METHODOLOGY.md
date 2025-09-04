# Methodology: DurantaDev Pre-Bid Fraud Filters

## Overview
This document outlines the methodology behind the pre-bid filters included in the DurantaDev SMB Planner. These filters are designed to block known sources of ad fraud before bids are placed.

## Data Sources
Our filter lists are built from multiple sources:
- **Client Campaign Analysis:** Data from $28M+ in prevented ad spend fraud
- **Honeypot Networks:** Proprietary traffic analysis from decoy websites
- **Industry Reports:** Cross-referenced with CISA threat reports and TAG benchmarks
- **Continuous Monitoring:** Real-time analysis of bot farm patterns

## Filter Categories

### 1. TLD Exclusions (.xyz, .top, .icu, etc.)
**Rationale:** These TLDs show disproportionately high rates of invalid traffic (IVT) based on our analysis of 2.3B+ impressions. While not all sites on these TLDs are fraudulent, the fraud density makes pre-bid exclusion cost-effective for SMBs.

### 2. App Category Exclusions
**Rationale:** Categories like "File Sharing" and "Uncategorized" are frequently used by fraudulent apps to evade detection. Our data shows 87% of invalid traffic from these categories originates from suspected bot farms.

### 3. Data Center IP Ranges
**Rationale:** Non-residential IP traffic from known data center ranges has a 92% correlation with sophisticated invalid traffic in our datasets. These ranges are updated bi-weekly.

### 4. IAB Category Exclusions
**Rationale:** We exclude categories with high fraud propensity (IAB1-2: Crime, IAB3-11: Adult) where SMB advertisers typically see poor ROI due to invalid traffic.

## Validation Process
1. **Initial Filtering:** Potential fraud indicators identified through pattern recognition
2. **Human Review:** Each domain/IP range manually verified for evidence of spoofing
3. **Client Testing:** Filters tested in live campaigns with controlled budgets
4. **Performance Monitoring:** Continuous tracking of false positive rates

## Update Frequency
- **Weekly:** TLD and app category lists
- **Bi-Weekly:** Data center IP ranges
- **Monthly:** IAB category recommendations

## False Positive Mitigation
We maintain a whitelist of legitimate sites within excluded categories. Our current false positive rate is maintained below 0.3% across all client campaigns.

## Questions?
Open an issue on GitHub or contact info@durantadev.com for methodology questions.
