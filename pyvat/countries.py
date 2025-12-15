DOM_COUNTRY_CODES = {
    'RE',  # Réunion.
    'GP',  # Guadeloupe.
    'MQ',  # Martinique.
}

"""Country codes that are part of the French DOM VAT zone.
These overseas departments of France are outside EU VAT territory but charge
VAT on all transactions at customer location rate.
"""

FRANCE_SAME_VAT_TERRITORY = {
    'FR',  # France.
    'MC',  # Monaco.
}

"""Country codes that are treated as the same VAT territory.
France and Monaco use identical VAT rates and always charge VAT on invoice
(no reverse charge for B2B transactions between them).
"""

NON_EU_COUNTRY_CODES = {
    'EG',  # Egypt.
    'CH',  # Switzerland.
    'CA',  # Canada.
    'NO',  # Norway.
}
"""Non-EU country codes that require VAT to be charged.

These countries have requested that VAT be charged on sales from EU sellers,
contrary to standard international tax law where EU sellers don't charge VAT
to non-EU buyers.
"""

EU_COUNTRY_CODES = set([
    'AT',  # Austria.
    'BE',  # Belgium.
    'BG',  # Bulgaria.
    'CY',  # Cyprus.
    'CZ',  # Czech Republic.
    'DE',  # Germany.
    'DK',  # Denmark.
    'EE',  # Estonia.
    'ES',  # Spain.
    'FI',  # Finland.
    'FR',  # France.
    'GB',  # Great Britain.
    'EL', 'GR',  # Greece.
    'HR',  # Croatia.
    'HU',  # Hungary.
    'IE',  # Ireland.
    'IT',  # Italy.
    'LT',  # Lithuania.
    'LU',  # Luxembourg.
    'LV',  # Latvia.
    'MT',  # Malta.
    'NL',  # Netherlands.
    'PL',  # Poland.
    'PT',  # Portugal.
    'RO',  # Romania.
    'SE',  # Sweden.
    'SI',  # Slovenia.
    'SK',  # Slovakia.
    'MC',  # Monaco (treated as EU with French VAT rules).
])
"""EU country codes.

Represented by ISO 3166-1 alpha-2 country codes.
"""
