import datetime
from decimal import Decimal
from .countries import EU_COUNTRY_CODES, DOM_COUNTRY_CODES, FRANCE_SAME_VAT_TERRITORY
from .item_type import ItemType
from .vat_charge import VatCharge, VatChargeAction
from .utils import ensure_decimal

JANUARY_1_2015 = datetime.date(2015, 1, 1)


class VatRules(object):
    """Base VAT rules for a country.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        """Get the VAT rate for an item type.

        :param item_type: Item type.
        :type item_type: ItemType
        :param postal_code: Postal code of the buyer's location, used for region-specific VAT rates.
        :type postal_code: str
        :returns: the VAT rate in percent.
        :rtype: decimal.Decimal
        """

        raise NotImplementedError()

    def get_sale_to_country_vat_charge(self,
                                       date,
                                       item_type,
                                       buyer,
                                       seller,
                                       postal_code=None):
        """Get the VAT charge for selling an item to a buyer in the country.

        :param date: Sale date.
        :type date: datetime.date
        :param item_type: Type of the item being sold.
        :type item_type: ItemType
        :param buyer: Buyer.
        :type buyer: Party
        :param seller: Seller.
        :type seller: Party
        :param postal_code: Postal code of the buyer's location, used for region-specific VAT rates.
        :type postal_code: str
        :rtype: VatCharge
        :raises NotImplementedError:
            if no explicit rules for selling to the given country from the
            given country exist. VAT charge determining falls back to testing
            rules for the country in which the seller resides if this is
            raised.
        """

        raise NotImplementedError()

    def get_sale_from_country_vat_charge(self,
                                         date,
                                         item_type,
                                         buyer,
                                         seller,
                                         postal_code=None):
        """Get the VAT charge for selling an item as a seller in the country.

        :param date: Sale date.
        :type date: datetime.date
        :param item_type: Type of the item being sold.
        :type item_type: ItemType
        :param buyer: Buyer.
        :type buyer: Party
        :param seller: Seller.
        :type seller: Party
        :param postal_code: Postal code of the buyer's location, used for region-specific VAT rates.
        :type postal_code: str
        :rtype: VatCharge
        :raises NotImplementedError:
            if no rules for selling from the given country to the given country
            exist.
        """

        raise NotImplementedError()


class EuVatRulesMixin(object):
    """Mixin for VAT rules in EU countries.
    """

    def get_sale_to_country_vat_charge(self,
                                       date,
                                       item_type,
                                       buyer,
                                       seller,
                                       postal_code=None):
        # We only support business sellers at this time.
        if not seller.is_business:
            raise NotImplementedError(
                'non-business sellers are currently not supported'
            )

        # If the seller resides in the same country as the buyer, we charge
        # VAT regardless of whether the buyer is a business or not. Similarly,
        # if the buyer is a consumer, we must charge VAT in the buyer's country
        # of residence.
        if seller.country_code == buyer.country_code or \
                (not buyer.is_business and date >= JANUARY_1_2015):
            return VatCharge(VatChargeAction.charge,
                             buyer.country_code,
                             self.get_vat_rate(item_type, postal_code))

        # EU consumers are charged VAT in the seller's country prior to January
        # 1st, 2015.
        if not buyer.is_business:
            # Fall back to the seller's VAT rules for this one.
            raise NotImplementedError()

        # EU businesses will never be charged VAT but must account for the VAT
        # by the reverse-charge mechanism.
        return VatCharge(VatChargeAction.reverse_charge,
                         buyer.country_code,
                         0)

    def get_sale_from_country_vat_charge(self,
                                         date,
                                         item_type,
                                         buyer,
                                         seller,
                                         postal_code=None):
        # We only support business sellers at this time.
        if not seller.is_business:
            raise NotImplementedError(
                'non-business sellers are currently not supported'
            )

        # If the buyer resides outside the EU, we do not have to charge VAT.
        if buyer.country_code not in EU_COUNTRY_CODES:
            return VatCharge(VatChargeAction.no_charge, buyer.country_code, 0)

        # Both businesses and consumers are charged VAT in the seller's
        # country if both seller and buyer reside in the same country.
        if buyer.country_code == seller.country_code:
            return VatCharge(VatChargeAction.charge,
                             seller.country_code,
                             self.get_vat_rate(item_type, postal_code))

        # Businesses in other EU countries are not charged VAT but are
        # responsible for accounting for the tax through the reverse-charge
        # mechanism.
        if buyer.is_business:
            return VatCharge(VatChargeAction.reverse_charge,
                             buyer.country_code,
                             0)

        # Consumers in other EU countries are charged VAT in their country of
        # residence after January 1st, 2015. Before this date, you charge VAT
        # in the country where the company is located.
        if date >= datetime.date(2015, 1, 1):
            buyer_rules = VAT_RULES[buyer.country_code]

            return VatCharge(VatChargeAction.charge,
                             buyer.country_code,
                             buyer_rules.get_vat_rate(item_type, postal_code))
        else:
            return VatCharge(VatChargeAction.charge,
                             seller.country_code,
                             self.get_vat_rate(item_type, postal_code))


class ConstantEuVatRateRules(EuVatRulesMixin):
    """VAT rules for a country with a constant VAT rate in the entiry country.
    """

    def __init__(self, vat_rate):
        self.vat_rate = ensure_decimal(vat_rate)

    def get_vat_rate(self, item_type, postal_code=None):
        return self.vat_rate


class AtVatRules(EuVatRulesMixin):
    """VAT rules for Austria.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.prepaid_broadcasting_service:
            return Decimal(10)
        elif item_type == ItemType.ebook:
            return Decimal(10)
        return Decimal(20)


class CzVatRules(ConstantEuVatRateRules):
    """VAT rules for Czech Republic.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(10)
        return super(CzVatRules, self).get_vat_rate(item_type, postal_code)


class BeVatRules(ConstantEuVatRateRules):
    """VAT rules for Belgium.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(6)
        return super(BeVatRules, self).get_vat_rate(item_type, postal_code)


class IeVatRules(ConstantEuVatRateRules):
    """VAT rules for Ireland.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(9)
        return super(IeVatRules, self).get_vat_rate(item_type, postal_code)


class FiVatRules(ConstantEuVatRateRules):
    """VAT rules for  Finland.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(10)
        return super(FiVatRules, self).get_vat_rate(item_type, postal_code)


class NlVatRules(ConstantEuVatRateRules):
    """VAT rules for Netherlands.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(9)
        return super(NlVatRules, self).get_vat_rate(item_type, postal_code)


class MtVatRules(ConstantEuVatRateRules):
    """VAT rules for Malta.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(5)
        return super(MtVatRules, self).get_vat_rate(item_type, postal_code)


class GreatBritainVatRules(object):
    """VAT rules for Great Britain (post-Brexit).

    Business requirements:
    - B2C: Charge 20% UK VAT on invoice
    - B2B: Use reverse charge mechanism (0% on invoice, buyer accounts VAT)
    - GB is no longer part of EU (Brexit)
    - VAT rate is 20% (same rate pre-Brexit and post-Brexit)
    - Rules are consistent for all dates
    """

    def __init__(self, vat_rate=20):
        self.vat_rate = ensure_decimal(vat_rate)

    def get_sale_to_country_vat_charge(self,
                                       date,
                                       item_type,
                                       buyer,
                                       seller,
                                       postal_code=None):
        """Get VAT charge when selling TO Great Britain.

        B2C: Charge 20% UK VAT
        B2B: Reverse charge (0% on invoice)
        """
        # We only support business sellers
        if not seller.is_business:
            raise NotImplementedError(
                'non-business sellers are currently not supported'
            )

        # B2C: Charge 20% UK VAT
        if not buyer.is_business:
            return VatCharge(VatChargeAction.charge,
                             buyer.country_code,
                             self.get_vat_rate(item_type, postal_code))

        # B2B: Reverse charge
        return VatCharge(VatChargeAction.reverse_charge,
                         buyer.country_code,
                         0)

    def get_sale_from_country_vat_charge(self,
                                        date,
                                        item_type,
                                        buyer,
                                        seller,
                                        postal_code=None):
        """Get VAT charge when selling FROM Great Britain.

        Not implemented - we only handle selling TO GB from other countries.
        """
        raise NotImplementedError()

    def get_vat_rate(self, item_type, postal_code=None):
        """Get UK VAT rate.

        Returns 20% (UK standard rate - same pre-Brexit and post-Brexit).
        """
        return self.vat_rate


class SeVatRules(ConstantEuVatRateRules):
    """VAT rules for Sweden.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(6)
        return super(SeVatRules, self).get_vat_rate(item_type, postal_code)


class HrVatRules(ConstantEuVatRateRules):
    """VAT rules for Croatia.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(5)
        return super(HrVatRules, self).get_vat_rate(item_type, postal_code)


class PtVatRules(ConstantEuVatRateRules):
    """VAT rules for Portugal.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(6)
        return super(PtVatRules, self).get_vat_rate(item_type, postal_code)


class FranceMonacoVatRules(EuVatRulesMixin):
    """VAT rules for France and Monaco.

    France and Monaco are treated as the same VAT territory:
    - Both use identical VAT rates (20% standard, with special rates for ebooks, etc.)
    - FR ↔ MC always charge VAT on invoice (no reverse charge for B2B)
    - Monaco uses French VAT system
    """

    def get_sale_to_country_vat_charge(self,
                                       date,
                                       item_type,
                                       buyer,
                                       seller,
                                       postal_code=None):
        # DOM sellers (RE, GP, MQ) always charge VAT at buyer's location rate
        if seller.country_code in DOM_COUNTRY_CODES:
            return VatCharge(VatChargeAction.charge,
                             buyer.country_code,
                             self.get_vat_rate(item_type, postal_code))

        # FR ↔ MC treated as same VAT territory
        # Both charge 20% VAT on invoice (no reverse charge for B2B)
        if seller.country_code in FRANCE_SAME_VAT_TERRITORY:
            return VatCharge(VatChargeAction.charge,
                             buyer.country_code,
                             self.get_vat_rate(item_type, postal_code))

        # Otherwise use standard EU rules
        return super(FranceMonacoVatRules, self).get_sale_to_country_vat_charge(
            date, item_type, buyer, seller, postal_code)

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type.is_broadcasting_service:
            return Decimal(10)
        if item_type == ItemType.ebook:
            return Decimal('5.5')
        if item_type == ItemType.enewspaper:
            return Decimal('2.1')
        return Decimal(20)


class ElVatRules(EuVatRulesMixin):
    """VAT rules for Greece.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        return Decimal(24)


class LuVatRules(EuVatRulesMixin):
    """VAT rules for Luxembourg.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type.is_broadcasting_service:
            return Decimal(3)
        elif item_type == ItemType.ebook:
            return Decimal(3)
        return Decimal(17)


class PlVatRules(EuVatRulesMixin):
    """VAT rules for Poland.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type.is_broadcasting_service:
            return Decimal(8)
        if item_type == ItemType.ebook:
            return Decimal(5)
        return Decimal(23)


class EsVatRules(EuVatRulesMixin):
    """VAT rules for Spain.
    
    Special VAT rules apply to certain regions:
    - Ceuta (postal codes starting with 51): 0% VAT
    - Melilla (postal codes starting with 52): 0% VAT
    - Las Palmas (postal codes starting with 35): 0% VAT
    - Tenerife (postal codes starting with 38): 0% VAT
    """

    def get_vat_rate(self, item_type, postal_code=None):
        # Check if the postal code is for a region with 0% VAT
        if postal_code:
            # Convert to string in case it's passed as a number
            postal_code = str(postal_code)
            
            # Ceuta (51XXX), Melilla (52XXX), Las Palmas (35XXX), Tenerife (38XXX)
            if postal_code.startswith(('51', '52', '35', '38')):
                return Decimal(0)
        
        # Standard VAT rates for Spain
        if item_type == ItemType.ebook:
            return Decimal(4)
        return Decimal(21)


class DeVatRules(EuVatRulesMixin):
    """VAT rules for Germany.
    """

    def get_vat_rate(self, item_type, postal_code=None):
        if item_type == ItemType.ebook:
            return Decimal(7)
        return Decimal(19)



class NonEuVatRules(object):
    """Base class for non-EU countries VAT rules.

    Provides default implementation for countries that charge VAT
    both when selling TO and FROM the country.

    Important: This class charges VAT for BOTH B2C and B2B transactions.
    There is NO exemption for business-to-business sales.
    """

    def __init__(self, vat_rate):
        """Initialize with a constant VAT rate.

        :param vat_rate: The VAT rate percentage for the country.
        :type vat_rate: int, float, or Decimal
        """
        self.vat_rate = ensure_decimal(vat_rate)

    def get_sale_to_country_vat_charge(self,
                                       date,
                                       item_type,
                                       buyer,
                                       seller,
                                       postal_code=None):
        """Get VAT charge when selling TO this country."""
        return VatCharge(VatChargeAction.charge,
                         buyer.country_code,
                         self.get_vat_rate(item_type, postal_code))

    def get_sale_from_country_vat_charge(self,
                                        date,
                                        item_type,
                                        buyer,
                                        seller,
                                        postal_code=None):
        """Get VAT charge when selling FROM this country."""
        return VatCharge(VatChargeAction.charge,
                         buyer.country_code,
                         self.get_vat_rate(item_type, postal_code))

    def get_vat_rate(self, item_type, postal_code=None):
        """Get the VAT rate for an item type.

        :param item_type: Item type.
        :type item_type: ItemType
        :param postal_code: Postal code (for region-specific rates).
        :type postal_code: str
        :returns: VAT rate in percent.
        :rtype: Decimal
        """
        return self.vat_rate


class FranceDomVatRules(object):
    """VAT rules for French overseas departments (DOM: RE, GP, MQ).

    Business requirements:
    - DOM is outside EU VAT territory but VAT is ALWAYS charged on invoice
    - VAT rate = customer location VAT rate
    - FR/MC/EU → DOM: Charge 8.5% (DOM rate)
    - DOM → FR/MC: Charge 20% (France rate)
    - DOM → EU: Charge destination EU rate
    - DOM → DOM: Charge 8.5% (DOM rate)
    - 2015 rule change does NOT affect DOM

    Key principle: Always charge VAT at BUYER's location rate on the invoice.
    """

    def __init__(self, vat_rate):
        self.vat_rate = ensure_decimal(vat_rate)

    def get_sale_to_country_vat_charge(self,
                                       date,
                                       item_type,
                                       buyer,
                                       seller,
                                       postal_code=None):
        """Get VAT charge when selling TO this DOM territory.

        Rule: Always charge DOM VAT (8.5%) when customer is in DOM.
        Applies to: FR → DOM, MC → DOM, EU → DOM, DOM → DOM
        """
        # Customer in DOM = charge DOM VAT (8.5%)
        return VatCharge(VatChargeAction.charge,
                         buyer.country_code,
                         self.get_vat_rate(item_type, postal_code))

    def get_sale_from_country_vat_charge(self,
                                        date,
                                        item_type,
                                        buyer,
                                        seller,
                                        postal_code=None):
        """Get VAT charge when selling FROM this DOM territory.

        Rule: Always charge VAT at customer location rate.
        - DOM → FR/MC: Charge 20% (France rate)
        - DOM → EU: Charge destination EU rate
        - DOM → DOM: Charge 8.5% (DOM rate)
        """
        # Get buyer's VAT rate from VAT_RULES
        buyer_rules = VAT_RULES[buyer.country_code]

        return VatCharge(VatChargeAction.charge,
                         buyer.country_code,
                         buyer_rules.get_vat_rate(item_type, postal_code))

    def get_vat_rate(self, item_type, postal_code=None):
        """Get the VAT rate for this territory (8.5%)."""
        return self.vat_rate


class EgVatRules(NonEuVatRules):
    """VAT rules for Egypt.

    Egypt requires 14% VAT to be charged on both B2C and B2B sales.
    B2B transactions are NOT exempt.
    """

    def __init__(self):
        super(EgVatRules, self).__init__(14)


class ChVatRules(NonEuVatRules):
    """VAT rules for Switzerland."""

    def __init__(self):
        super(ChVatRules, self).__init__(Decimal('8.1'))


class CanadaVatRules(NonEuVatRules):
    """VAT rules for Canada."""

    def __init__(self):
        super(CanadaVatRules, self).__init__(0)


class NorwayVatRules(NonEuVatRules):
    """VAT rules for Norway."""

    def __init__(self):
        super(NorwayVatRules, self).__init__(25)



# VAT rates updated July 1st 2025
VAT_RULES = {
    'AT': AtVatRules(),
    'BE': BeVatRules(21),
    'BG': ConstantEuVatRateRules(20),
    'CY': ConstantEuVatRateRules(19),
    'CZ': CzVatRules(21),
    'DE': DeVatRules(),
    'DK': ConstantEuVatRateRules(25),
    'EE': ConstantEuVatRateRules(24),
    'EL': ElVatRules(),
    'GR': ElVatRules(),  # Synonymous country code for Greece
    'ES': EsVatRules(),
    'FI': FiVatRules(25.5),
    'FR': FranceMonacoVatRules(),
    'GB': GreatBritainVatRules(20),
    'HR': HrVatRules(25),
    'HU': ConstantEuVatRateRules(27),
    'IE': IeVatRules(23),
    'IT': ConstantEuVatRateRules(22),
    'LT': ConstantEuVatRateRules(21),
    'LU': LuVatRules(),
    'LV': ConstantEuVatRateRules(21),
    'MT': MtVatRules(18),
    'NL': NlVatRules(21),
    'PL': PlVatRules(),
    'PT': PtVatRules(23),
    'RO': ConstantEuVatRateRules(21),
    'SE': SeVatRules(25),
    'SK': ConstantEuVatRateRules(23),
    'SI': ConstantEuVatRateRules(22),
    'EG': EgVatRules(),
    'CH': ChVatRules(),
    'CA': CanadaVatRules(),
    'NO': NorwayVatRules(),
    'MC': FranceMonacoVatRules(),  # Monaco uses same VAT rules as France
    'RE': FranceDomVatRules(Decimal('8.5')),  # Réunion (French overseas department)
    'GP': FranceDomVatRules(Decimal('8.5')),  # Guadeloupe (French overseas department)
    'MQ': FranceDomVatRules(Decimal('8.5')),  # Martinique (French overseas department)
}

"""VAT rules by country.

Maps an ISO 3316 alpha-2 country code to the VAT rules applicable in the given
country.
"""
