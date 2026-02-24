import datetime
import pycountry
from decimal import Decimal
from pyvat import (
    get_sale_vat_charge,
    ItemType,
    Party,
    VatChargeAction,
)
from pyvat.countries import (EU_COUNTRY_CODES, NON_EU_COUNTRY_CODES,
                             DOM_COUNTRY_CODES, FRANCE_SAME_VAT_TERRITORY)
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
        ItemType.generic_broadcasting_service: Decimal(10),
        ItemType.prepaid_broadcasting_service: Decimal(10),
        ItemType.ebook: Decimal('5.5'),
        ItemType.enewspaper: Decimal('2.1'),
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

                # Skip FR ↔ MC: treated as same VAT territory (tested separately)
                if seller_cc in FRANCE_SAME_VAT_TERRITORY and buyer_cc in FRANCE_SAME_VAT_TERRITORY:
                    continue

                # Skip DOM ↔ DOM and DOM ↔ FR/MC (tested separately)
                if (seller_cc in DOM_COUNTRY_CODES and
                    (buyer_cc in DOM_COUNTRY_CODES or buyer_cc in FRANCE_SAME_VAT_TERRITORY)):
                    continue
                if buyer_cc in DOM_COUNTRY_CODES and seller_cc in FRANCE_SAME_VAT_TERRITORY:
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

                # Skip FR ↔ MC: treated as same VAT territory (always charge VAT)
                if (seller_cc == 'FR' and buyer_cc == 'MC') or \
                   (seller_cc == 'MC' and buyer_cc == 'FR'):
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

                # Skip FR/MC ↔ DOM transactions (tested separately)
                if (seller_cc in FRANCE_SAME_VAT_TERRITORY and buyer_cc in DOM_COUNTRY_CODES):
                    continue
                if (seller_cc in DOM_COUNTRY_CODES and buyer_cc in FRANCE_SAME_VAT_TERRITORY):
                    continue

                # Skip DOM ↔ DOM transactions (tested separately)
                if seller_cc in DOM_COUNTRY_CODES and buyer_cc in DOM_COUNTRY_CODES:
                    continue

                # Skip DOM territories as buyers (tested separately)
                if buyer_cc in DOM_COUNTRY_CODES:
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
                                # Egypt: B2B is exempt (0%), B2C charges 14%
                                if buyer_cc == 'EG' and buyer_is_business:
                                    self.assertEqual(vat_charge.action,
                                                     VatChargeAction.no_charge)
                                    self.assertEqual(vat_charge.rate, Decimal(0))
                                else:
                                    self.assertEqual(vat_charge.action,
                                                     VatChargeAction.charge)
                                    # Verify correct VAT rate is charged
                                    if buyer_cc in EXPECTED_VAT_RATES:
                                        self.assertEqual(vat_charge.rate,
                                                         EXPECTED_VAT_RATES[buyer_cc][it])
                            # Great Britain (post-Brexit): B2C charges 20%, B2B uses reverse charge
                            elif buyer_cc == 'GB':
                                if buyer_is_business:
                                    self.assertEqual(vat_charge.action,
                                                     VatChargeAction.reverse_charge)
                                    self.assertEqual(vat_charge.rate, Decimal(0))
                                else:
                                    self.assertEqual(vat_charge.action,
                                                     VatChargeAction.charge)
                                    self.assertEqual(vat_charge.rate, Decimal(20))
                            else:
                                # Standard behavior: EU doesn't charge VAT to non-EU
                                self.assertEqual(vat_charge.action,
                                                 VatChargeAction.no_charge)
                                self.assertEqual(vat_charge.rate, Decimal(0))

    def test_french_vat_zone_transactions(self):
        """Test VAT charge for DOM territories.

        Key rules:
        1. VAT is ALWAYS charged on invoice
        2. VAT rate = customer location VAT rate
        3. DOM is unaffected by 2015 change
        4. Monaco treated exactly like France
        """

        # A. FR/MC → DOM: Charge 8.5% (DOM rate)
        for seller_cc in FRANCE_SAME_VAT_TERRITORY:
            for buyer_cc in DOM_COUNTRY_CODES:
                with self.subTest(scenario=f"{seller_cc} → {buyer_cc}"):
                    vat_charge = get_sale_vat_charge(
                        datetime.date(2015, 1, 1),
                        ItemType.generic_electronic_service,
                        Party(country_code=buyer_cc, is_business=True),
                        Party(country_code=seller_cc, is_business=True)
                    )
                    self.assertEqual(vat_charge.action, VatChargeAction.charge,
                                    f"{seller_cc} to {buyer_cc} should charge VAT")
                    self.assertEqual(vat_charge.rate, Decimal('8.5'),
                                    f"{seller_cc} to {buyer_cc} should charge DOM rate (8.5%)")
                    self.assertEqual(vat_charge.country_code, buyer_cc)

        # B. DOM → FR/MC: Charge 20% (France rate)
        for seller_cc in DOM_COUNTRY_CODES:
            for buyer_cc in FRANCE_SAME_VAT_TERRITORY:
                with self.subTest(scenario=f"{seller_cc} → {buyer_cc}"):
                    vat_charge = get_sale_vat_charge(
                        datetime.date(2015, 1, 1),
                        ItemType.generic_electronic_service,
                        Party(country_code=buyer_cc, is_business=True),
                        Party(country_code=seller_cc, is_business=True)
                    )
                    self.assertEqual(vat_charge.action, VatChargeAction.charge,
                                    f"{seller_cc} to {buyer_cc} should charge VAT")
                    self.assertEqual(vat_charge.rate, Decimal('20'),
                                    f"{seller_cc} to {buyer_cc} should charge France rate (20%)")
                    self.assertEqual(vat_charge.country_code, buyer_cc)

        # C. DOM → DOM: Charge 8.5% (DOM rate)
        vat_charge = get_sale_vat_charge(
            datetime.date(2015, 1, 1),
            ItemType.generic_electronic_service,
            Party(country_code='GP', is_business=True),
            Party(country_code='RE', is_business=True)
        )
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.rate, Decimal('8.5'))
        self.assertEqual(vat_charge.country_code, 'GP')

        # D. EU → DOM: Charge 8.5% (DOM rate)
        vat_charge = get_sale_vat_charge(
            datetime.date(2015, 1, 1),
            ItemType.generic_electronic_service,
            Party(country_code='RE', is_business=True),
            Party(country_code='DE', is_business=True)
        )
        self.assertEqual(vat_charge.action, VatChargeAction.charge,
                        "DE to RE should charge VAT")
        self.assertEqual(vat_charge.rate, Decimal('8.5'),
                        "DE to RE should charge DOM rate (8.5%)")
        self.assertEqual(vat_charge.country_code, 'RE')

        # E. DOM → EU: Charge destination EU rate (19% for Germany)
        vat_charge = get_sale_vat_charge(
            datetime.date(2015, 1, 1),
            ItemType.generic_electronic_service,
            Party(country_code='DE', is_business=False),  # Consumer
            Party(country_code='RE', is_business=True)
        )
        self.assertEqual(vat_charge.action, VatChargeAction.charge,
                        "RE to DE should charge VAT")
        self.assertEqual(vat_charge.rate, Decimal('19'),
                        "RE to DE should charge Germany rate (19%)")
        self.assertEqual(vat_charge.country_code, 'DE')

        # F. Verify DOM is unaffected by 2015 change
        # Before 2015: Still charge 8.5% for FR → DOM
        vat_charge = get_sale_vat_charge(
            datetime.date(2014, 12, 15),
            ItemType.generic_electronic_service,
            Party(country_code='RE', is_business=False),
            Party(country_code='FR', is_business=True)
        )
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.rate, Decimal('8.5'),
                        "FR to RE before 2015 should still charge DOM rate (8.5%)")

        # Before 2015: Still charge 20% for DOM → FR
        vat_charge = get_sale_vat_charge(
            datetime.date(2014, 12, 15),
            ItemType.generic_electronic_service,
            Party(country_code='FR', is_business=False),
            Party(country_code='RE', is_business=True)
        )
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.rate, Decimal('20'),
                        "RE to FR before 2015 should still charge France rate (20%)")

        # G. FR ↔ MC: Same VAT territory (always charge 20% VAT)
        # FR → MC: Always charge 20% (both B2B and B2C)
        for buyer_type in [True, False]:  # Business and Consumer
            vat_charge = get_sale_vat_charge(
                datetime.date(2015, 1, 1),
                ItemType.generic_electronic_service,
                Party(country_code='MC', is_business=buyer_type),
                Party(country_code='FR', is_business=True)
            )
            buyer_label = "B2B" if buyer_type else "B2C"
            self.assertEqual(vat_charge.action, VatChargeAction.charge,
                            f"FR to MC ({buyer_label}) should charge VAT")
            self.assertEqual(vat_charge.rate, Decimal('20'),
                            f"FR to MC ({buyer_label}) should charge 20%")

        # MC → FR: Always charge 20% (both B2B and B2C)
        for buyer_type in [True, False]:  # Business and Consumer
            vat_charge = get_sale_vat_charge(
                datetime.date(2015, 1, 1),
                ItemType.generic_electronic_service,
                Party(country_code='FR', is_business=buyer_type),
                Party(country_code='MC', is_business=True)
            )
            buyer_label = "B2B" if buyer_type else "B2C"
            self.assertEqual(vat_charge.action, VatChargeAction.charge,
                            f"MC to FR ({buyer_label}) should charge VAT")
            self.assertEqual(vat_charge.rate, Decimal('20'),
                            f"MC to FR ({buyer_label}) should charge 20%")

    def test_great_britain_vat_rules(self):
        """Test Great Britain VAT rules (post-Brexit).

        Key rules:
        1. GB is no longer part of EU (Brexit)
        2. B2C: Charge 20% UK VAT on invoice
        3. B2B: Use reverse charge (0% on invoice, buyer accounts VAT)
        4. Rules are consistent for all dates
        5. VAT rate is 20% (same rate pre-Brexit and post-Brexit)
        """

        # Test B2C: France → Great Britain consumer
        # Should charge 20% UK VAT
        vat_charge = get_sale_vat_charge(
            datetime.date(2025, 12, 15),
            ItemType.generic_electronic_service,
            Party(country_code='GB', is_business=False),  # Consumer
            Party(country_code='FR', is_business=True)
        )
        self.assertEqual(vat_charge.action, VatChargeAction.charge,
                        "FR to GB (B2C) should charge VAT")
        self.assertEqual(vat_charge.rate, Decimal('20'),
                        "FR to GB (B2C) should charge 20% UK VAT")
        self.assertEqual(vat_charge.country_code, 'GB')

        # Test B2B: France → Great Britain business
        # Should use reverse charge
        vat_charge = get_sale_vat_charge(
            datetime.date(2025, 12, 15),
            ItemType.generic_electronic_service,
            Party(country_code='GB', is_business=True),  # Business
            Party(country_code='FR', is_business=True)
        )
        self.assertEqual(vat_charge.action, VatChargeAction.reverse_charge,
                        "FR to GB (B2B) should use reverse charge")
        self.assertEqual(vat_charge.rate, Decimal('0'),
                        "FR to GB (B2B) should be 0% (reverse charge)")
        self.assertEqual(vat_charge.country_code, 'GB')

        # Test that rules are consistent across different dates
        for test_date in [datetime.date(2020, 1, 1),   # Pre-Brexit
                          datetime.date(2021, 1, 1),   # Post-Brexit
                          datetime.date(2025, 12, 15)]:  # Current

            # B2C should always charge 20%
            vat_charge_b2c = get_sale_vat_charge(
                test_date,
                ItemType.generic_electronic_service,
                Party(country_code='GB', is_business=False),
                Party(country_code='FR', is_business=True)
            )
            self.assertEqual(vat_charge_b2c.action, VatChargeAction.charge,
                            f"B2C should charge VAT on {test_date}")
            self.assertEqual(vat_charge_b2c.rate, Decimal('20'),
                            f"B2C should charge 20% on {test_date}")

            # B2B should always use reverse charge
            vat_charge_b2b = get_sale_vat_charge(
                test_date,
                ItemType.generic_electronic_service,
                Party(country_code='GB', is_business=True),
                Party(country_code='FR', is_business=True)
            )
            self.assertEqual(vat_charge_b2b.action, VatChargeAction.reverse_charge,
                            f"B2B should use reverse charge on {test_date}")
            self.assertEqual(vat_charge_b2b.rate, Decimal('0'),
                            f"B2B should be 0% on {test_date}")




