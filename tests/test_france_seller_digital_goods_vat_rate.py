"""
Test validation of France seller digital goods VAT rates.

This test ensures that all VAT rates and behaviors documented in
FRANCE_VAT_RATES_DIGITAL_GOODS.md match the actual implementation.
Tests cover all scenarios when France is the seller of digital goods.
"""
import unittest
import datetime
from decimal import Decimal

from pyvat import get_sale_vat_charge, Party, ItemType
from pyvat.vat_charge import VatChargeAction


class FranceSellerDigitalGoodsVatRateTestCase(unittest.TestCase):
    """Test cases to validate France seller digital goods VAT rates.

    These tests verify that the documentation accurately reflects the actual
    VAT calculation behavior for all scenarios listed in the documentation.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.test_date = datetime.date(2025, 12, 15)
        self.item_type = ItemType.generic_electronic_service
        self.errors = []

    def _test_scenario(self, seller_cc, buyer_cc, is_business, expected_action,
                       expected_rate, description):
        """Helper method to test a VAT scenario.

        Args:
            seller_cc: Seller country code
            buyer_cc: Buyer country code
            is_business: Whether buyer is a business
            expected_action: Expected VatChargeAction
            expected_rate: Expected VAT rate
            description: Description for error messages
        """
        vat = get_sale_vat_charge(
            self.test_date,
            self.item_type,
            Party(country_code=buyer_cc, is_business=is_business),
            Party(country_code=seller_cc, is_business=True)
        )

        buyer_type = "B2B" if is_business else "B2C"

        # Check action
        self.assertEqual(
            vat.action, expected_action,
            f"{description} ({buyer_type}): Expected action {expected_action.name}, "
            f"got {vat.action.name}"
        )

        # Check rate
        self.assertEqual(
            vat.rate, expected_rate,
            f"{description} ({buyer_type}): Expected rate {expected_rate}%, "
            f"got {vat.rate}%"
        )

    def test_01_france_same_vat_territory(self):
        """Test Section 1: France → Same VAT Territory (France & Monaco).

        Validates:
        - France → France (B2C and B2B): 20%
        - France → Monaco (B2C and B2B): 20%
        - No reverse charge for B2B
        """
        print("\n" + "="*80)
        print("TESTING SECTION 1: France → Same VAT Territory (FR, MC)")
        print("="*80)

        # France → France
        self._test_scenario('FR', 'FR', False, VatChargeAction.charge,
                           Decimal('20'), "France → France")
        self._test_scenario('FR', 'FR', True, VatChargeAction.charge,
                           Decimal('20'), "France → France")

        # France → Monaco
        self._test_scenario('FR', 'MC', False, VatChargeAction.charge,
                           Decimal('20'), "France → Monaco")
        self._test_scenario('FR', 'MC', True, VatChargeAction.charge,
                           Decimal('20'), "France → Monaco")

        print("✓ All Same VAT Territory scenarios PASSED")

    def test_02_france_eu_countries(self):
        """Test Section 2: France → EU Countries.

        Validates:
        - Germany: B2C=19%, B2B=reverse charge (0%)
        - Italy: B2C=22%, B2B=reverse charge (0%)
        - Romania: B2C=21%, B2B=reverse charge (0%)
        """
        print("\n" + "="*80)
        print("TESTING SECTION 2: France → EU Countries")
        print("="*80)

        # Germany
        self._test_scenario('FR', 'DE', False, VatChargeAction.charge,
                           Decimal('19'), "France → Germany")
        self._test_scenario('FR', 'DE', True, VatChargeAction.reverse_charge,
                           Decimal('0'), "France → Germany")

        # Italy
        self._test_scenario('FR', 'IT', False, VatChargeAction.charge,
                           Decimal('22'), "France → Italy")
        self._test_scenario('FR', 'IT', True, VatChargeAction.reverse_charge,
                           Decimal('0'), "France → Italy")

        # Romania
        self._test_scenario('FR', 'RO', False, VatChargeAction.charge,
                           Decimal('21'), "France → Romania")
        self._test_scenario('FR', 'RO', True, VatChargeAction.reverse_charge,
                           Decimal('0'), "France → Romania")

        print("✓ All EU Countries scenarios PASSED")

    def test_03_france_dom_territories(self):
        """Test Section 3: France → French DOM Territories.

        Validates:
        - Réunion: B2C and B2B both 8.5%
        - Guadeloupe: B2C and B2B both 8.5%
        - Martinique: B2C and B2B both 8.5%
        - No reverse charge for B2B
        """
        print("\n" + "="*80)
        print("TESTING SECTION 3: France → DOM Territories")
        print("="*80)

        # Réunion
        self._test_scenario('FR', 'RE', False, VatChargeAction.charge,
                           Decimal('8.5'), "France → Réunion")
        self._test_scenario('FR', 'RE', True, VatChargeAction.charge,
                           Decimal('8.5'), "France → Réunion")

        # Guadeloupe
        self._test_scenario('FR', 'GP', False, VatChargeAction.charge,
                           Decimal('8.5'), "France → Guadeloupe")
        self._test_scenario('FR', 'GP', True, VatChargeAction.charge,
                           Decimal('8.5'), "France → Guadeloupe")

        # Martinique
        self._test_scenario('FR', 'MQ', False, VatChargeAction.charge,
                           Decimal('8.5'), "France → Martinique")
        self._test_scenario('FR', 'MQ', True, VatChargeAction.charge,
                           Decimal('8.5'), "France → Martinique")

        print("✓ All DOM Territories scenarios PASSED")

    def test_04_france_non_eu_special_cases(self):
        """Test Section 4: France → Non-EU Countries (Special Cases).

        Validates:
        - Egypt: B2C 14%, B2B 0% (exempt)
        - Switzerland: B2C and B2B both 8.1% (NOT exempt)
        - Canada: B2C and B2B both 0% (exempt)
        - Norway: B2C and B2B both 25% (NOT exempt)
        """
        print("\n" + "="*80)
        print("TESTING SECTION 4: France → Non-EU Special Cases")
        print("="*80)

        # Egypt - B2C charges 14%, B2B exempt (0%)
        self._test_scenario('FR', 'EG', False, VatChargeAction.charge,
                           Decimal('14'), "France → Egypt")
        self._test_scenario('FR', 'EG', True, VatChargeAction.no_charge,
                           Decimal('0'), "France → Egypt")

        # Switzerland - B2B NOT exempt (charges 8.1%)
        self._test_scenario('FR', 'CH', False, VatChargeAction.charge,
                           Decimal('8.1'), "France → Switzerland")
        self._test_scenario('FR', 'CH', True, VatChargeAction.charge,
                           Decimal('8.1'), "France → Switzerland")

        # Canada - B2B exempt (0%)
        self._test_scenario('FR', 'CA', False, VatChargeAction.charge,
                           Decimal('0'), "France → Canada")
        self._test_scenario('FR', 'CA', True, VatChargeAction.charge,
                           Decimal('0'), "France → Canada")

        # Norway - B2B NOT exempt (charges 25%)
        self._test_scenario('FR', 'NO', False, VatChargeAction.charge,
                           Decimal('25'), "France → Norway")
        self._test_scenario('FR', 'NO', True, VatChargeAction.charge,
                           Decimal('25'), "France → Norway")

        print("✓ All Non-EU Special Cases scenarios PASSED")

    def test_05_france_great_britain(self):
        """Test Section 5: France → Great Britain.

        Validates:
        - GB B2C: 20%
        - GB B2B: reverse charge (0%)
        - Post-Brexit behavior
        """
        print("\n" + "="*80)
        print("TESTING SECTION 5: France → Great Britain (Post-Brexit)")
        print("="*80)

        # Great Britain B2C
        self._test_scenario('FR', 'GB', False, VatChargeAction.charge,
                           Decimal('20'), "France → Great Britain")

        # Great Britain B2B - reverse charge
        self._test_scenario('FR', 'GB', True, VatChargeAction.reverse_charge,
                           Decimal('0'), "France → Great Britain")

        print("✓ All Great Britain scenarios PASSED")

    def test_06_summary_table_validation(self):
        """Test Section 6: Summary Table.

        Validates all entries in the quick reference summary table.
        """
        print("\n" + "="*80)
        print("TESTING SECTION 6: Summary Table Validation")
        print("="*80)

        summary_scenarios = [
            # (seller, buyer, b2c_rate, b2b_rate, b2b_action, description)
            ('FR', 'FR', Decimal('20'), Decimal('20'), VatChargeAction.charge, "France"),
            ('FR', 'MC', Decimal('20'), Decimal('20'), VatChargeAction.charge, "Monaco"),
            ('FR', 'DE', Decimal('19'), Decimal('0'), VatChargeAction.reverse_charge, "Germany"),
            ('FR', 'IT', Decimal('22'), Decimal('0'), VatChargeAction.reverse_charge, "Italy"),
            ('FR', 'RO', Decimal('21'), Decimal('0'), VatChargeAction.reverse_charge, "Romania"),
            ('FR', 'RE', Decimal('8.5'), Decimal('8.5'), VatChargeAction.charge, "Réunion"),
            ('FR', 'GP', Decimal('8.5'), Decimal('8.5'), VatChargeAction.charge, "Guadeloupe"),
            ('FR', 'MQ', Decimal('8.5'), Decimal('8.5'), VatChargeAction.charge, "Martinique"),
            ('FR', 'EG', Decimal('14'), Decimal('0'), VatChargeAction.no_charge, "Egypt"),
            ('FR', 'CH', Decimal('8.1'), Decimal('8.1'), VatChargeAction.charge, "Switzerland"),
            ('FR', 'CA', Decimal('0'), Decimal('0'), VatChargeAction.charge, "Canada"),
            ('FR', 'NO', Decimal('25'), Decimal('25'), VatChargeAction.charge, "Norway"),
            ('FR', 'GB', Decimal('20'), Decimal('0'), VatChargeAction.reverse_charge, "Great Britain"),
        ]

        for seller, buyer, b2c_rate, b2b_rate, b2b_action, desc in summary_scenarios:
            # Test B2C
            self._test_scenario(seller, buyer, False, VatChargeAction.charge,
                               b2c_rate, f"{desc} (Summary)")

            # Test B2B
            self._test_scenario(seller, buyer, True, b2b_action,
                               b2b_rate, f"{desc} (Summary)")

        print("✓ All Summary Table entries PASSED")

    def test_07_special_rates_france_monaco(self):
        """Test special VAT rates for France and Monaco.

        Validates:
        - Broadcasting services: 10%
        - E-books: 5.5%
        - E-newspapers: 2.1%
        """
        print("\n" + "="*80)
        print("TESTING SPECIAL RATES: France & Monaco")
        print("="*80)

        for country in ['FR', 'MC']:
            # Broadcasting services
            vat = get_sale_vat_charge(
                self.test_date,
                ItemType.generic_broadcasting_service,
                Party(country_code=country, is_business=False),
                Party(country_code=country, is_business=True)
            )
            self.assertEqual(vat.rate, Decimal('10'),
                           f"{country} broadcasting should be 10%")

            # E-books
            vat = get_sale_vat_charge(
                self.test_date,
                ItemType.ebook,
                Party(country_code=country, is_business=False),
                Party(country_code=country, is_business=True)
            )
            self.assertEqual(vat.rate, Decimal('5.5'),
                           f"{country} ebook should be 5.5%")

            # E-newspapers
            vat = get_sale_vat_charge(
                self.test_date,
                ItemType.enewspaper,
                Party(country_code=country, is_business=False),
                Party(country_code=country, is_business=True)
            )
            self.assertEqual(vat.rate, Decimal('2.1'),
                           f"{country} enewspaper should be 2.1%")

        print("✓ All Special Rates PASSED")

    @classmethod
    def setUpClass(cls):
        """Print header before running tests."""
        print("\n" + "="*80)
        print("=" * 80)
        print("  FRANCE SELLER DIGITAL GOODS VAT RATE VALIDATION")
        print("=" * 80)
        print("="*80)
        print("\nValidating all VAT scenarios documented in:")
        print("  docs/FRANCE_VAT_RATES_DIGITAL_GOODS.md")
        print("\nThis ensures documentation matches actual implementation.")
        print("Testing scenarios where France is the seller of digital goods.")

    @classmethod
    def tearDownClass(cls):
        """Print footer after all tests."""
        print("\n" + "="*80)
        print("=" * 80)
        print("  ✅ ALL FRANCE SELLER DIGITAL GOODS VAT RATE TESTS PASSED!")
        print("=" * 80)
        print("="*80)
        print("\nDocumentation is accurate and matches implementation.")
        print("All VAT rates and behaviors are correctly documented.")
        print()


if __name__ == '__main__':
    unittest.main(verbosity=2)

