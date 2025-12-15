# France VAT Rates for Digital Goods

**Seller: France**  
**Products: Digital goods (electronic services, telecommunications, broadcasting)**  
**Date: December 15, 2025**

---

## Table of Contents

1. [France → Same VAT Territory (France & Monaco)](#1-france--same-vat-territory)
2. [France → EU Countries](#2-france--eu-countries)
3. [France → French DOM Territories](#3-france--french-dom-territories)
4. [France → Non-EU Countries (Special Cases)](#4-france--non-eu-countries-special-cases)
5. [France → Great Britain](#5-france--great-britain)
6. [Summary Table](#6-summary-table)

---

## 1. France → Same VAT Territory

**Countries**: France (FR), Monaco (MC)

| Country | Buyer Type | VAT Action | VAT Rate | Charged In | Notes |
|---------|------------|------------|----------|------------|-------|
| **France** | B2C (Consumer) | Charge | **20%** | FR | Standard rate |
| **France** | B2B (Business) | Charge | **20%** | FR | Same country |
| **Monaco** | B2C (Consumer) | Charge | **20%** | MC | Same VAT territory |
| **Monaco** | B2B (Business) | Charge | **20%** | MC | No reverse charge |

**Key Points:**
- France and Monaco are treated as the **same VAT territory**
- **Always charge 20% VAT on invoice** (even for B2B)
- **No reverse charge** for B2B transactions
- Monaco uses identical VAT rates as France

**Special Rates (France & Monaco):**
- Broadcasting services: 10%
- E-books: 5.5%
- E-newspapers: 2.1%
- Standard digital services: 20%

---

## 2. France → EU Countries

**Example Countries**: Germany (DE), Italy (IT), Romania (RO)

| Country | Buyer Type | VAT Action | VAT Rate | Charged In | Notes |
|---------|------------|------------|----------|------------|-------|
| **Germany** | B2C (Consumer) | Charge | **19%** | DE | Customer location rate |
| **Germany** | B2B (Business) | Reverse Charge | **0%** | DE | Business self-accounts |
| **Italy** | B2C (Consumer) | Charge | **22%** | IT | Customer location rate |
| **Italy** | B2B (Business) | Reverse Charge | **0%** | IT | Business self-accounts |
| **Romania** | B2C (Consumer) | Charge | **21%** | RO | Customer location rate |
| **Romania** | B2B (Business) | Reverse Charge | **0%** | RO | Business self-accounts |

**Key Points:**
- **B2C**: VAT charged at customer's country rate (after Jan 1, 2015)
- **B2B**: Reverse charge mechanism (0% on invoice, business pays VAT)
- Standard EU cross-border rules apply

**EU Country VAT Rates (Standard):**
- Germany: 19%
- Italy: 22%
- Romania: 21%
- Spain: 21%
- Belgium: 21%
- Netherlands: 21%

---

## 3. France → French DOM Territories

**Countries**: Réunion (RE), Guadeloupe (GP), Martinique (MQ)

| Country | Buyer Type | VAT Action | VAT Rate | Charged In | Notes |
|---------|------------|------------|----------|------------|-------|
| **Réunion** | B2C (Consumer) | Charge | **8.5%** | RE | DOM rate |
| **Réunion** | B2B (Business) | Charge | **8.5%** | RE | DOM rate |
| **Guadeloupe** | B2C (Consumer) | Charge | **8.5%** | GP | DOM rate |
| **Guadeloupe** | B2B (Business) | Charge | **8.5%** | GP | DOM rate |
| **Martinique** | B2C (Consumer) | Charge | **8.5%** | MQ | DOM rate |
| **Martinique** | B2B (Business) | Charge | **8.5%** | MQ | DOM rate |

**Key Points:**
- DOM territories are **outside EU VAT territory**
- **Always charge 8.5% VAT on invoice** (customer location rate)
- No reverse charge for B2B
- DOM rate is 8.5% (reduced rate compared to France's 20%)
- Not affected by 2015 EU rule change

**Important:**
- VAT is charged at the **buyer's location** (DOM rate: 8.5%)
- Different from France's standard 20% rate
- Applies to all digital goods uniformly

---

## 4. France → Non-EU Countries (Special Cases)

**Countries**: Egypt (EG), Switzerland (CH), Canada (CA), Norway (NO)

| Country | Buyer Type | VAT Action | VAT Rate | Charged In | Notes |
|---------|------------|------------|----------|------------|-------|
| **Egypt** | B2C (Consumer) | Charge | **14%** | EG | Government mandate |
| **Egypt** | B2B (Business) | No Charge | **0%** | - | B2B exempt |
| **Switzerland** | B2C (Consumer) | Charge | **8.1%** | CH | Government mandate |
| **Switzerland** | B2B (Business) | Charge | **8.1%** | CH | B2B NOT exempt |
| **Canada** | B2C (Consumer) | No Charge | **0%** | - | No VAT on invoice |
| **Canada** | B2B (Business) | No Charge | **0%** | - | B2B exempt |
| **Norway** | B2C (Consumer) | Charge | **25%** | NO | Government mandate |
| **Norway** | B2B (Business) | Charge | **25%** | NO | B2B NOT exempt |

**Key Points:**
- These countries have **special requirements** contrary to standard international tax law
- Normally, EU sellers don't charge VAT to non-EU buyers
- These countries have requested VAT be charged
- **Egypt & Canada**: B2B transactions are exempt
- **Switzerland & Norway**: B2B transactions are NOT exempt (must charge VAT)

**VAT Rates:**
- Egypt: 14%
- Switzerland: 8.1%
- Canada: 0% (standard non-EU treatment)
- Norway: 25%

---

## 5. France → Great Britain

**Country**: Great Britain (GB)

| Country | Buyer Type | VAT Action | VAT Rate | Charged In | Notes |
|---------|------------|------------|----------|------------|-------|
| **Great Britain** | B2C (Consumer) | Charge | **20%** | GB | Post-Brexit rules |
| **Great Britain** | B2B (Business) | Reverse Charge | **0%** | GB | Business self-accounts |

**Key Points:**
- Great Britain is **in EU_COUNTRY_CODES** (system still treats as EU)
- VAT rate: 20%
- B2C: Charge VAT at GB rate (20%)
- B2B: Reverse charge mechanism applies
- Post-Brexit, GB may have different rules in practice, but system treats it as EU

**Note:** After Brexit (2020), Great Britain is no longer in the EU, but the system currently includes it in `EU_COUNTRY_CODES` for VAT calculation purposes.

---

## 6. Summary Table

### Quick Reference: France Selling Digital Goods

| Destination | B2C VAT | B2B VAT | Special Notes |
|-------------|---------|---------|---------------|
| **France** | 20% | 20% | Same country |
| **Monaco** | 20% | 20% | Same VAT territory, no reverse charge |
| **Germany** | 19% | 0% (RC) | Standard EU rules |
| **Italy** | 22% | 0% (RC) | Standard EU rules |
| **Romania** | 21% | 0% (RC) | Standard EU rules |
| **Réunion** | 8.5% | 8.5% | DOM - outside EU, always charge |
| **Guadeloupe** | 8.5% | 8.5% | DOM - outside EU, always charge |
| **Martinique** | 8.5% | 8.5% | DOM - outside EU, always charge |
| **Egypt** | 14% | 0% | Special mandate, B2B exempt |
| **Switzerland** | 8.1% | 8.1% | Special mandate, B2B NOT exempt |
| **Canada** | 0% | 0% | Standard non-EU |
| **Norway** | 25% | 25% | Special mandate, B2B NOT exempt |
| **Great Britain** | 20% | 0% (RC) | Treated as EU in system |

**Legend:**
- **RC** = Reverse Charge (0% on invoice, buyer pays VAT)
- **DOM** = French Overseas Departments
- **B2C** = Business to Consumer
- **B2B** = Business to Business

---

## Invoice Examples

### Example 1: France → Monaco (B2B)
```
Product: Digital Service
Price: €100.00
VAT (20%): €20.00
Total: €120.00

Note: VAT charged on invoice (no reverse charge)
```

### Example 2: France → Germany (B2B)
```
Product: Digital Service
Price: €100.00
VAT: €0.00 (Reverse Charge)
Total: €100.00

Note: German business pays VAT themselves
```

### Example 3: France → Réunion (B2C)
```
Product: Digital Service
Price: €100.00
VAT (8.5%): €8.50
Total: €108.50

Note: DOM rate applies (customer location)
```

### Example 4: France → Norway (B2B)
```
Product: Digital Service
Price: €100.00
VAT (25%): €25.00
Total: €125.00

Note: Norway requires VAT even for B2B
```

### Example 5: France → Italy (B2C)
```
Product: Digital Service
Price: €100.00
VAT (22%): €22.00
Total: €122.00

Note: Italian VAT rate applies
```

---

## Additional Information

### 2015 EU VAT Rule Change

On **January 1, 2015**, the EU changed VAT rules for B2C digital goods:
- **Before 2015**: VAT charged at seller's country rate
- **After 2015**: VAT charged at customer's country rate

**Exception**: DOM territories are **NOT affected** by this change. They always use customer location rate.

### Key Territories Explained

1. **Same VAT Territory (FR, MC)**
   - Treated as domestic transactions
   - No reverse charge for B2B
   - Always charge 20% VAT

2. **DOM Territories (RE, GP, MQ)**
   - Outside EU VAT territory
   - Always charge VAT on invoice
   - Use 8.5% DOM rate
   - Not affected by 2015 change

3. **Standard EU Countries**
   - B2C: Charge at destination rate
   - B2B: Reverse charge (0% on invoice)

4. **Non-EU Special Cases**
   - Egypt, Switzerland, Norway, Canada
   - Each has unique requirements
   - Some charge B2B, some don't

---

## Implementation Notes

This VAT rate table is based on the pyvat library implementation as of December 15, 2025.

**Country Code Sets:**
- `FRANCE_SAME_VAT_TERRITORY`: `{'FR', 'MC'}`
- `DOM_COUNTRY_CODES`: `{'RE', 'GP', 'MQ'}`
- `NON_EU_COUNTRY_CODES`: `{'EG', 'CH', 'CA', 'NO'}`
- `EU_COUNTRY_CODES`: All EU members including MC and GB

For complete implementation details, see:
- `pyvat/countries.py` - Country code definitions
- `pyvat/vat_rules.py` - VAT calculation logic
- `tests/test_sale_vat_charge.py` - Test cases and examples

---

**Last Updated:** December 15, 2025  
**Seller Country:** France (FR)  
**Product Type:** Digital Goods (Electronic Services)

