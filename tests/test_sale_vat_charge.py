import datetime
import pycountry
from decimal import Decimal
from pyvat import (
    get_sale_vat_charge,
    ItemType,
    Party,
    VatChargeAction,
)
from pyvat.countries import EU_COUNTRY_CODES, FRANCE_COUNTRY_CODES, NON_EU_COUNTRY_CODES
try:
    from unittest2 import TestCase
except ImportError:
    from unittest import TestCase

EXPECTED_VAT_RATES = {
    'AT': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(10),
        ItemType.ebook: Decimal(10),
        ItemType.enewspaper: Decimal(20),
    },
    'BE': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(6),
        ItemType.enewspaper: Decimal(21),
    },
    'BG': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(20),
        ItemType.ebook: Decimal(20),
        ItemType.enewspaper: Decimal(20),
    },
    'CY': {
        ItemType.generic_physical_good: Decimal(19),
        ItemType.generic_electronic_service: Decimal(19),
        ItemType.generic_telecommunications_service: Decimal(19),
        ItemType.generic_broadcasting_service: Decimal(19),
        ItemType.prepaid_broadcasting_service: Decimal(19),
        ItemType.ebook: Decimal(19),
        ItemType.enewspaper: Decimal(19),
    },
    'CZ': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(10),
        ItemType.enewspaper: Decimal(21),
    },
    'DE': {
        ItemType.generic_physical_good: Decimal(19),
        ItemType.generic_electronic_service: Decimal(19),
        ItemType.generic_telecommunications_service: Decimal(19),
        ItemType.generic_broadcasting_service: Decimal(19),
        ItemType.prepaid_broadcasting_service: Decimal(19),
        ItemType.ebook: Decimal(7),
        ItemType.enewspaper: Decimal(19),
    },
    'DK': {
        ItemType.generic_physical_good: Decimal(25),
        ItemType.generic_electronic_service: Decimal(25),
        ItemType.generic_telecommunications_service: Decimal(25),
        ItemType.generic_broadcasting_service: Decimal(25),
        ItemType.prepaid_broadcasting_service: Decimal(25),
        ItemType.ebook: Decimal(25),
        ItemType.enewspaper: Decimal(25),
    },
    'EE': {
        ItemType.generic_physical_good: Decimal(24),
        ItemType.generic_electronic_service: Decimal(24),
        ItemType.generic_telecommunications_service: Decimal(24),
        ItemType.generic_broadcasting_service: Decimal(24),
        ItemType.prepaid_broadcasting_service: Decimal(24),
        ItemType.ebook: Decimal(24),
        ItemType.enewspaper: Decimal(24),
    },
    'ES': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(4),
        ItemType.enewspaper: Decimal(21),
    },
    'FI': {
        ItemType.generic_physical_good: Decimal(25.5),
        ItemType.generic_electronic_service: Decimal(25.5),
        ItemType.generic_telecommunications_service: Decimal(25.5),
        ItemType.generic_broadcasting_service: Decimal(25.5),
        ItemType.prepaid_broadcasting_service: Decimal(25.5),
        ItemType.ebook: Decimal(10),
        ItemType.enewspaper: Decimal(25.5),
    },
    'FR': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(10),
        ItemType.prepaid_broadcasting_service: Decimal(10),
        ItemType.ebook: Decimal('5.5'),
        ItemType.enewspaper: Decimal('2.1'),
    },
    'EL': {
        ItemType.generic_physical_good: Decimal(24),
        ItemType.generic_electronic_service: Decimal(24),
        ItemType.generic_telecommunications_service: Decimal(24),
        ItemType.generic_broadcasting_service: Decimal(24),
        ItemType.prepaid_broadcasting_service: Decimal(24),
        ItemType.ebook: Decimal(24),
        ItemType.enewspaper: Decimal(24),
    },
    'GB': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(20),
        ItemType.ebook: Decimal(20),
        ItemType.enewspaper: Decimal(20),
    },
    'GR': {  # Synonymous for "EL" -- Greece
        ItemType.generic_physical_good: Decimal(24),
        ItemType.generic_electronic_service: Decimal(24),
        ItemType.generic_telecommunications_service: Decimal(24),
        ItemType.generic_broadcasting_service: Decimal(24),
        ItemType.prepaid_broadcasting_service: Decimal(24),
        ItemType.ebook: Decimal(24),
        ItemType.enewspaper: Decimal(24),
    },
    'HR': {
        ItemType.generic_physical_good: Decimal(25),
        ItemType.generic_electronic_service: Decimal(25),
        ItemType.generic_telecommunications_service: Decimal(25),
        ItemType.generic_broadcasting_service: Decimal(25),
        ItemType.prepaid_broadcasting_service: Decimal(25),
        ItemType.ebook: Decimal(5),
        ItemType.enewspaper: Decimal(25),
    },
    'HU': {
        ItemType.generic_physical_good: Decimal(27),
        ItemType.generic_electronic_service: Decimal(27),
        ItemType.generic_telecommunications_service: Decimal(27),
        ItemType.generic_broadcasting_service: Decimal(27),
        ItemType.prepaid_broadcasting_service: Decimal(27),
        ItemType.ebook: Decimal(27),
        ItemType.enewspaper: Decimal(27),
    },
    'IE': {
        ItemType.generic_physical_good: Decimal(23),
        ItemType.generic_electronic_service: Decimal(23),
        ItemType.generic_telecommunications_service: Decimal(23),
        ItemType.generic_broadcasting_service: Decimal(23),
        ItemType.prepaid_broadcasting_service: Decimal(23),
        ItemType.ebook: Decimal(9),
        ItemType.enewspaper: Decimal(23),
    },
    'IT': {
        ItemType.generic_physical_good: Decimal(22),
        ItemType.generic_electronic_service: Decimal(22),
        ItemType.generic_telecommunications_service: Decimal(22),
        ItemType.generic_broadcasting_service: Decimal(22),
        ItemType.prepaid_broadcasting_service: Decimal(22),
        ItemType.ebook: Decimal(22),
        ItemType.enewspaper: Decimal(22),
    },
    'LT': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(21),
        ItemType.enewspaper: Decimal(21),
    },
    'LU': {
        ItemType.generic_physical_good: Decimal(17),
        ItemType.generic_electronic_service: Decimal(17),
        ItemType.generic_telecommunications_service: Decimal(17),
        ItemType.generic_broadcasting_service: Decimal(3),
        ItemType.prepaid_broadcasting_service: Decimal(3),
        ItemType.ebook: Decimal(3),
        ItemType.enewspaper: Decimal(17),
    },
    'LV': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(21),
        ItemType.enewspaper: Decimal(21),
    },
    'MT': {
        ItemType.generic_physical_good: Decimal(18),
        ItemType.generic_electronic_service: Decimal(18),
        ItemType.generic_telecommunications_service: Decimal(18),
        ItemType.generic_broadcasting_service: Decimal(18),
        ItemType.prepaid_broadcasting_service: Decimal(18),
        ItemType.ebook: Decimal(5),
        ItemType.enewspaper: Decimal(18),
    },
    'NL': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(9),
        ItemType.enewspaper: Decimal(21),
    },
    'PL': {
        ItemType.generic_physical_good: Decimal(23),
        ItemType.generic_electronic_service: Decimal(23),
        ItemType.generic_telecommunications_service: Decimal(23),
        ItemType.generic_broadcasting_service: Decimal(8),
        ItemType.prepaid_broadcasting_service: Decimal(8),
        ItemType.ebook: Decimal(5),
        ItemType.enewspaper: Decimal(23),
    },
    'PT': {
        ItemType.generic_physical_good: Decimal(23),
        ItemType.generic_electronic_service: Decimal(23),
        ItemType.generic_telecommunications_service: Decimal(23),
        ItemType.generic_broadcasting_service: Decimal(23),
        ItemType.prepaid_broadcasting_service: Decimal(23),
        ItemType.ebook: Decimal(6),
        ItemType.enewspaper: Decimal(23),
    },
    'RO': {
        ItemType.generic_physical_good: Decimal(21),
        ItemType.generic_electronic_service: Decimal(21),
        ItemType.generic_telecommunications_service: Decimal(21),
        ItemType.generic_broadcasting_service: Decimal(21),
        ItemType.prepaid_broadcasting_service: Decimal(21),
        ItemType.ebook: Decimal(21),
        ItemType.enewspaper: Decimal(21),
    },
    'SE': {
        ItemType.generic_physical_good: Decimal(25),
        ItemType.generic_electronic_service: Decimal(25),
        ItemType.generic_telecommunications_service: Decimal(25),
        ItemType.generic_broadcasting_service: Decimal(25),
        ItemType.prepaid_broadcasting_service: Decimal(25),
        ItemType.ebook: Decimal(6),
        ItemType.enewspaper: Decimal(25),
    },
    'SI': {
        ItemType.generic_physical_good: Decimal(22),
        ItemType.generic_electronic_service: Decimal(22),
        ItemType.generic_telecommunications_service: Decimal(22),
        ItemType.generic_broadcasting_service: Decimal(22),
        ItemType.prepaid_broadcasting_service: Decimal(22),
        ItemType.ebook: Decimal(22),
        ItemType.enewspaper: Decimal(22),
    },
    'SK': {
        ItemType.generic_physical_good: Decimal(23),
        ItemType.generic_electronic_service: Decimal(23),
        ItemType.generic_telecommunications_service: Decimal(23),
        ItemType.generic_broadcasting_service: Decimal(23),
        ItemType.prepaid_broadcasting_service: Decimal(23),
        ItemType.ebook: Decimal(23),
        ItemType.enewspaper: Decimal(23),
    },
    # Non-EU countries that require VAT charge
    'EG': {
        ItemType.generic_physical_good: Decimal(14),
        ItemType.generic_electronic_service: Decimal(14),
        ItemType.generic_telecommunications_service: Decimal(14),
        ItemType.generic_broadcasting_service: Decimal(14),
        ItemType.prepaid_broadcasting_service: Decimal(14),
        ItemType.ebook: Decimal(14),
        ItemType.enewspaper: Decimal(14),
    },
    'CH': {
        ItemType.generic_physical_good: Decimal('8.1'),
        ItemType.generic_electronic_service: Decimal('8.1'),
        ItemType.generic_telecommunications_service: Decimal('8.1'),
        ItemType.generic_broadcasting_service: Decimal('8.1'),
        ItemType.prepaid_broadcasting_service: Decimal('8.1'),
        ItemType.ebook: Decimal('8.1'),
        ItemType.enewspaper: Decimal('8.1'),
    },
    'CA': {
        ItemType.generic_physical_good: Decimal(0),
        ItemType.generic_electronic_service: Decimal(0),
        ItemType.generic_telecommunications_service: Decimal(0),
        ItemType.generic_broadcasting_service: Decimal(0),
        ItemType.prepaid_broadcasting_service: Decimal(0),
        ItemType.ebook: Decimal(0),
        ItemType.enewspaper: Decimal(0),
    },
    'NO': {
        ItemType.generic_physical_good: Decimal(25),
        ItemType.generic_electronic_service: Decimal(25),
        ItemType.generic_telecommunications_service: Decimal(25),
        ItemType.generic_broadcasting_service: Decimal(25),
        ItemType.prepaid_broadcasting_service: Decimal(25),
        ItemType.ebook: Decimal(25),
        ItemType.enewspaper: Decimal(25),
    },
    'MC': {
        ItemType.generic_physical_good: Decimal(20),
        ItemType.generic_electronic_service: Decimal(20),
        ItemType.generic_telecommunications_service: Decimal(20),
        ItemType.generic_broadcasting_service: Decimal(20),
        ItemType.prepaid_broadcasting_service: Decimal(20),
        ItemType.ebook: Decimal(20),
        ItemType.enewspaper: Decimal(20),
    },
    'RE': {
        ItemType.generic_physical_good: Decimal('8.5'),
        ItemType.generic_electronic_service: Decimal('8.5'),
        ItemType.generic_telecommunications_service: Decimal('8.5'),
        ItemType.generic_broadcasting_service: Decimal('8.5'),
        ItemType.prepaid_broadcasting_service: Decimal('8.5'),
        ItemType.ebook: Decimal('8.5'),
        ItemType.enewspaper: Decimal('8.5'),
    },
    'GP': {
        ItemType.generic_physical_good: Decimal('8.5'),
        ItemType.generic_electronic_service: Decimal('8.5'),
        ItemType.generic_telecommunications_service: Decimal('8.5'),
        ItemType.generic_broadcasting_service: Decimal('8.5'),
        ItemType.prepaid_broadcasting_service: Decimal('8.5'),
        ItemType.ebook: Decimal('8.5'),
        ItemType.enewspaper: Decimal('8.5'),
    },
    'MQ': {
        ItemType.generic_physical_good: Decimal('8.5'),
        ItemType.generic_electronic_service: Decimal('8.5'),
        ItemType.generic_telecommunications_service: Decimal('8.5'),
        ItemType.generic_broadcasting_service: Decimal('8.5'),
        ItemType.prepaid_broadcasting_service: Decimal('8.5'),
        ItemType.ebook: Decimal('8.5'),
        ItemType.enewspaper: Decimal('8.5'),
    },
}
SUPPORTED_ITEM_TYPES = [
    ItemType.generic_electronic_service,
    ItemType.generic_telecommunications_service,
    ItemType.generic_broadcasting_service,
    ItemType.prepaid_broadcasting_service,
    ItemType.ebook,
    ItemType.enewspaper,
]


class GetSaleVatChargeTestCase(TestCase):
    """Test case for :func:`get_sale_vat_charge`.
    """
    
    def test_spanish_regional_vat_rates(self):
        """Test that Spanish regions with special VAT rules return the correct VAT rate.
        """
        # Test regions with 0% VAT
        special_regions = {
            '51001': 'Ceuta',
            '52001': 'Melilla',
            '35001': 'Las Palmas',
            '38001': 'Tenerife'
        }
        
        for postal_code, region_name in special_regions.items():
            for it in SUPPORTED_ITEM_TYPES:
                vat_charge = get_sale_vat_charge(
                    datetime.date.today(),
                    it,
                    Party(country_code='ES', is_business=False),
                    Party(country_code='ES', is_business=True),
                    postal_code=postal_code
                )
                self.assertEqual(vat_charge.action, VatChargeAction.charge)
                self.assertEqual(vat_charge.rate, Decimal(0),
                                f"Expected 0% VAT for {region_name} (postal code: {postal_code})")
                self.assertEqual(vat_charge.country_code, 'ES')
        
        # Test standard Spanish VAT rates (without special postal codes)
        for it in SUPPORTED_ITEM_TYPES:
            vat_charge = get_sale_vat_charge(
                datetime.date.today(),
                it,
                Party(country_code='ES', is_business=False),
                Party(country_code='ES', is_business=True)
            )
            self.assertEqual(vat_charge.action, VatChargeAction.charge)
            self.assertEqual(vat_charge.rate, EXPECTED_VAT_RATES['ES'][it])
            self.assertEqual(vat_charge.country_code, 'ES')
    
    def test_get_sale_vat_charge(self):
        """get_sale_vat_charge(..)
        """

        # EU businesses selling to any type of customer in their own country
        # charge VAT.
        for seller_cc in EU_COUNTRY_CODES:
            for it in SUPPORTED_ITEM_TYPES:
                for d in [datetime.date(2014, 12, 15),
                          datetime.date(2015, 1, 1)]:
                    for buyer_is_business in [True, False]:
                        vat_charge = get_sale_vat_charge(
                            d,
                            it,
                            Party(country_code=seller_cc,
                                  is_business=buyer_is_business),
                            Party(country_code=seller_cc, is_business=True)
                        )
                        self.assertEqual(vat_charge.action,
                                         VatChargeAction.charge)

                        self.assertEqual(vat_charge.rate,
                                         EXPECTED_VAT_RATES[seller_cc][it])
                        self.assertEqual(vat_charge.country_code,
                                         seller_cc)

        # EU businesses selling to businesses in other EU countries apply the
        # reverse-charge mechanism.
        # Note: French VAT zone (FR, MC, RE, GP, MQ) is tested separately in
        # test_french_vat_zone_transactions() and skipped here.

        for seller_cc in EU_COUNTRY_CODES:
            for buyer_cc in EU_COUNTRY_CODES:
                if seller_cc == buyer_cc:
                    continue

                # Skip French VAT zone internal transactions (tested separately)
                if seller_cc in FRANCE_COUNTRY_CODES and buyer_cc in FRANCE_COUNTRY_CODES:
                    continue

                for it in SUPPORTED_ITEM_TYPES:
                    for d in [datetime.date(2014, 12, 15),
                              datetime.date(2015, 1, 1)]:
                        vat_charge = get_sale_vat_charge(
                            d,
                            it,
                            Party(country_code=buyer_cc, is_business=True),
                            Party(country_code=seller_cc, is_business=True)
                        )
                        self.assertEqual(vat_charge.action,
                                         VatChargeAction.reverse_charge)
                        self.assertEqual(vat_charge.rate,
                                         Decimal(0))
                        self.assertEqual(vat_charge.country_code,
                                         buyer_cc)

        # EU businesses selling to consumers in other EU countries charge VAT
        # in the country in which the consumer resides after January 1st, 2015.
        for seller_cc in EU_COUNTRY_CODES:
            for buyer_cc in EU_COUNTRY_CODES:
                if seller_cc == buyer_cc:
                    continue

                for it in SUPPORTED_ITEM_TYPES:
                    for d in [datetime.date(2014, 12, 15),
                              datetime.date(2015, 1, 1)]:
                        vat_charge = get_sale_vat_charge(
                            d,
                            it,
                            Party(country_code=buyer_cc, is_business=False),
                            Party(country_code=seller_cc, is_business=True)
                        )
                        self.assertEqual(vat_charge.action,
                                         VatChargeAction.charge)
                        self.assertEqual(
                            vat_charge.rate,
                            EXPECTED_VAT_RATES[buyer_cc][it]
                            if d >= datetime.date(2015, 1, 1) else
                            EXPECTED_VAT_RATES[seller_cc][it]
                        )
                        self.assertEqual(
                            vat_charge.country_code,
                            buyer_cc
                            if d >= datetime.date(2015, 1, 1) else
                            seller_cc
                        )

        # EU businesses selling to customers outside the EU do not charge VAT.
        # EXCEPTION: Some countries (EG, CH, CA, NO) require
        # VAT to be charged even when seller is from EU (per government request).

        for seller_cc in EU_COUNTRY_CODES:
            for buyer_country in pycountry.countries:
                buyer_cc = buyer_country.alpha_2
                if buyer_cc in EU_COUNTRY_CODES:
                    continue

                for it in SUPPORTED_ITEM_TYPES:
                    for d in [datetime.date(2014, 12, 15),
                              datetime.date(2015, 1, 1)]:
                        for buyer_is_business in [True, False]:
                            vat_charge = get_sale_vat_charge(
                                d,
                                it,
                                Party(country_code=buyer_cc,
                                      is_business=buyer_is_business),
                                Party(country_code=seller_cc, is_business=True)
                            )

                            # New countries require VAT charge per government mandate
                            if buyer_cc in NON_EU_COUNTRY_CODES:
                                self.assertEqual(vat_charge.action,
                                                 VatChargeAction.charge)
                                # Verify correct VAT rate is charged
                                if buyer_cc in EXPECTED_VAT_RATES:
                                    self.assertEqual(vat_charge.rate,
                                                     EXPECTED_VAT_RATES[buyer_cc][it])
                            else:
                                # Standard behavior: EU doesn't charge VAT to non-EU
                                self.assertEqual(vat_charge.action,
                                                 VatChargeAction.no_charge)
                                self.assertEqual(vat_charge.rate, Decimal(0))

    def test_french_vat_zone_transactions(self):
        """Test VAT charge for France selling to French overseas departments.
        France (FR) selling to Monaco (MC), Réunion (RE), Guadeloupe (GP), 
        and Martinique (MQ) should charge VAT at the buyer's country rate,
        not use reverse charge mechanism (treated as one VAT zone).
        """
        test_cases = [
            # (seller, buyer, expected_rate, description)
            ('FR', 'MC', Decimal(20), 'France to Monaco'),
            ('FR', 'RE', Decimal('8.5'), 'France to Réunion'),
            ('FR', 'GP', Decimal('8.5'), 'France to Guadeloupe'),
            ('FR', 'MQ', Decimal('8.5'), 'France to Martinique'),
        ]
        # Test B2B transactions
        for seller_cc, buyer_cc, expected_rate, description in test_cases:
            with self.subTest(scenario=f"B2B: {description}"):
                vat_charge = get_sale_vat_charge(
                    datetime.date(2015, 1, 1),
                    ItemType.generic_electronic_service,
                    Party(country_code=buyer_cc, is_business=True),
                    Party(country_code=seller_cc, is_business=True)
                )
                # Should charge VAT, NOT reverse charge
                self.assertEqual(vat_charge.action, VatChargeAction.charge,
                                f"{description} B2B should charge VAT")
                self.assertEqual(vat_charge.rate, expected_rate,
                                f"{description} B2B should charge buyer's rate")
                self.assertEqual(vat_charge.country_code, buyer_cc,
                                f"{description} B2B should use buyer's country")
        # Test B2C transactions (after 2015-01-01)
        for seller_cc, buyer_cc, expected_rate, description in test_cases:
            with self.subTest(scenario=f"B2C (2015+): {description}"):
                vat_charge = get_sale_vat_charge(
                    datetime.date(2015, 1, 1),
                    ItemType.generic_electronic_service,
                    Party(country_code=buyer_cc, is_business=False),
                    Party(country_code=seller_cc, is_business=True)
                )
                # Should charge VAT at buyer's country rate
                self.assertEqual(vat_charge.action, VatChargeAction.charge,
                                f"{description} B2C should charge VAT")
                self.assertEqual(vat_charge.rate, expected_rate,
                                f"{description} B2C should charge buyer's rate")
                self.assertEqual(vat_charge.country_code, buyer_cc,
                                f"{description} B2C should use buyer's country")
        # Test B2C transactions before 2015-01-01 (should use seller's rate)
        seller_rates = {
            'FR': Decimal(20),
            'MC': Decimal(20),
            'RE': Decimal('8.5'),
            'GP': Decimal('8.5'),
            'MQ': Decimal('8.5'),
        }
        for seller_cc, buyer_cc, _, description in test_cases[:4]:
            with self.subTest(scenario=f"B2C (2014): {description}"):
                vat_charge = get_sale_vat_charge(
                    datetime.date(2014, 12, 15),
                    ItemType.generic_electronic_service,
                    Party(country_code=buyer_cc, is_business=False),
                    Party(country_code=seller_cc, is_business=True)
                )
                # Before 2015, should charge at seller's rate
                self.assertEqual(vat_charge.action, VatChargeAction.charge,
                                f"{description} B2C (2014) should charge VAT")
                self.assertEqual(vat_charge.rate, seller_rates[seller_cc],
                                f"{description} B2C (2014) should charge seller's rate")
                self.assertEqual(vat_charge.country_code, seller_cc,
                                f"{description} B2C (2014) should use seller's country")
