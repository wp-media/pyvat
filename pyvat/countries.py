FRANCE_COUNTRY_CODES = {
    'FR',  # France.
    'MC',  # Monaco (French VAT zone).
    'RE',  # Réunion (French overseas department).
    'GP',  # Guadeloupe (French overseas department).
    'MQ',  # Martinique (French overseas department).
}
"""Country codes that are part of the French VAT zone.

France and its territories are treated as one VAT zone for the purposes of VAT
calculation. This includes mainland France and various overseas departments.
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
    'RE',  # Réunion (French Overseas Department).
    'GP',  # Guadeloupe (French Overseas Department).
    'MQ',  # Martinique (French Overseas Department).
])
"""EU country codes.

Represented by ISO 3166-1 alpha-2 country codes.
"""
