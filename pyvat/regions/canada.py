"""Canadian provincial tax data indexed by postal code prefix.

PROVINCE_RATES is a dict keyed by postal code prefix:

    {
        'M': ProvinceRate(prefix='M', province='Ontario',          rate=Decimal('13'), tax_types=(HST,)),
        'V': ProvinceRate(prefix='V', province='British Columbia', rate=Decimal('12'), tax_types=(GST, PST)),
        'G': ProvinceRate(prefix='G', province='Quebec',           rate=Decimal('5'),  tax_types=(GST,)),
        'T': ProvinceRate(prefix='T', province='Alberta',          rate=Decimal('5'),  tax_types=(GST,)),
        ...
    }

Lookup by postal code prefix:

    from pyvat.regions.canada import PROVINCE_RATES

    info = PROVINCE_RATES.get('M5V 3L9'[0].upper())
    # ProvinceRate(prefix='M', province='Ontario', rate=Decimal('13'), tax_types=('HST',))
"""

from decimal import Decimal
from typing import Dict, NamedTuple, Tuple

from pyvat.vat_rules import CanadaVatRules

# ---------------------------------------------------------------------------
# Tax type constants
# ---------------------------------------------------------------------------

GST = "GST"
HST = "HST"
PST = "PST"
QST = "QST"
RST = "RST"


class ProvinceRate(NamedTuple):
    prefix: str
    province: str
    rate: Decimal
    tax_types: Tuple[str, ...]


_PROVINCE_META = (
    ("A", "Newfoundland and Labrador", (HST,)),
    ("B", "Nova Scotia", (HST,)),
    ("C", "Prince Edward Island", (HST,)),
    ("E", "New Brunswick", (HST,)),
    ("G", "Quebec", (GST,)),  # not registered for QST
    ("H", "Quebec", (GST,)),  # not registered for QST
    ("J", "Quebec", (GST,)),  # not registered for QST
    ("K", "Ontario", (HST,)),
    ("L", "Ontario", (HST,)),
    ("M", "Ontario", (HST,)),
    ("N", "Ontario", (HST,)),
    ("P", "Ontario", (HST,)),
    ("R", "Manitoba", (GST,)),  # not registered for RST
    ("S", "Saskatchewan", (GST, PST)),
    ("T", "Alberta", (GST,)),
    ("V", "British Columbia", (GST, PST)),
    ("X", "Northwest Territories and Nunavut", (GST,)),
    ("Y", "Yukon", (GST,)),
)

PROVINCE_RATES: Dict[str, ProvinceRate] = {
    prefix: ProvinceRate(
        prefix=prefix,
        province=province,
        rate=CanadaVatRules.PROVINCE_VAT_RATES[prefix],
        tax_types=tax_types,
    )
    for prefix, province, tax_types in _PROVINCE_META
}


def get_province_info(postal_code):
    if not isinstance(postal_code, str) or len(postal_code.strip()) == 0:
        raise ValueError("postal_code must be a non-empty string")

    postal_code_prefix = postal_code[0].upper()
    info = PROVINCE_RATES.get(postal_code_prefix)
    return info
