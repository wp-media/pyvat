from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, NamedTuple, Optional, Tuple

from pyvat.vat_rules import CanadaVatRules

# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------


class RegionRules(ABC):
    """Base class for country-specific region rules.

    Subclass this for each country that requires region-level tax logic
    (e.g. provinces, states, cantons).  Each subclass is responsible for
    mapping a postal / zip code to a rate and a region descriptor.
    """

    @abstractmethod
    def get_rate(self, postal_code: Optional[str] = None) -> Decimal:
        """Return the applicable tax rate for the given postal code.

        Falls back to the country default when *postal_code* is absent or
        unrecognised.
        """

    @abstractmethod
    def get_region(self, postal_code: Optional[str] = None):
        """Return the region descriptor for the given postal code, or ``None``."""


# ---------------------------------------------------------------------------
# Canada
# ---------------------------------------------------------------------------


class CanadaRegionRules(RegionRules):
    """Region-specific tax rules for Canada.

    The rate is determined by the first letter of the postal code.
    Falls back to Ontario (13 %) when no postal code is provided.
    """

    # Tax type constants
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

    DEFAULT_RATE: Decimal = CanadaVatRules.DEFAULT_VAT_RATE

    # Populated after the class body — ProvinceRate and the tax-type constants
    # are not accessible inside a class-body comprehension in Python 3.
    PROVINCE_RATES: Dict[str, "CanadaRegionRules.ProvinceRate"] = {}

    def get_rate(self, postal_code: Optional[str] = None) -> Decimal:
        """Return the combined tax rate for the given Canadian postal code.

        :param postal_code: Canadian postal code. Only the first character is
            used to determine the province. Falls back to Ontario (13 %) when
            absent or unrecognised.
        :returns: Combined tax rate in percent (e.g. ``Decimal('13')``).
        """
        region = self.get_region(postal_code)
        return region.rate if region is not None else self.DEFAULT_RATE

    def get_region(
        self, postal_code: Optional[str] = None
    ) -> Optional["CanadaRegionRules.ProvinceRate"]:
        """Return the province data for the given Canadian postal code.

        :param postal_code: Canadian postal code. Only the first character is
            used to determine the province.
        :returns: :class:`ProvinceRate` for the matching province, or ``None``
            when *postal_code* is absent or the prefix is unrecognised.

            The returned :class:`ProvinceRate` contains:

            - ``prefix`` — single uppercase letter identifying the province
              (e.g. ``'M'`` for Ontario).
            - ``province`` — full province or territory name
              (e.g. ``'Ontario'``).
            - ``rate`` — combined tax rate in percent as a
              :class:`~decimal.Decimal` (e.g. ``Decimal('13')``).
            - ``tax_types`` — tuple of applicable tax-type constants indicating
              how the rate is composed (e.g. ``(HST,)`` for a single harmonised
              levy or ``(GST, PST)`` for two separate components).
        """
        if not postal_code:
            return None
        prefix = str(postal_code).strip().upper()[0]
        return self.PROVINCE_RATES.get(prefix)


CanadaRegionRules.PROVINCE_RATES = {
    prefix: CanadaRegionRules.ProvinceRate(
        prefix=prefix,
        province=province,
        rate=CanadaVatRules.PROVINCE_VAT_RATES[prefix],
        tax_types=tax_types,
    )
    for prefix, province, tax_types in (
        ("A", "Newfoundland and Labrador", (CanadaRegionRules.HST,)),
        ("B", "Nova Scotia", (CanadaRegionRules.HST,)),
        ("C", "Prince Edward Island", (CanadaRegionRules.HST,)),
        ("E", "New Brunswick", (CanadaRegionRules.HST,)),
        ("G", "Quebec", (CanadaRegionRules.GST,)),  # not registered for QST
        ("H", "Quebec", (CanadaRegionRules.GST,)),  # not registered for QST
        ("J", "Quebec", (CanadaRegionRules.GST,)),  # not registered for QST
        ("K", "Ontario", (CanadaRegionRules.HST,)),
        ("L", "Ontario", (CanadaRegionRules.HST,)),
        ("M", "Ontario", (CanadaRegionRules.HST,)),
        ("N", "Ontario", (CanadaRegionRules.HST,)),
        ("P", "Ontario", (CanadaRegionRules.HST,)),
        ("R", "Manitoba", (CanadaRegionRules.GST,)),  # not registered for RST
        ("S", "Saskatchewan", (CanadaRegionRules.GST, CanadaRegionRules.PST)),
        ("T", "Alberta", (CanadaRegionRules.GST,)),
        ("V", "British Columbia", (CanadaRegionRules.GST, CanadaRegionRules.PST)),
        ("X", "Northwest Territories and Nunavut", (CanadaRegionRules.GST,)),
        ("Y", "Yukon", (CanadaRegionRules.GST,)),
    )
}
