import datetime
from decimal import Decimal
from unittest import TestCase
from pyvat import (
    get_sale_vat_charge,
    ItemType,
    Party,
    VatChargeAction,
)


class SpanishRegionVatTestCase(TestCase):
    """Test cases for Spanish region-specific VAT rates."""

    def setUp(self):
        self.sale_date = datetime.date(2024, 1, 1)
        self.german_seller = Party('DE', True)  # German business seller

    def test_spanish_special_regions_zero_vat(self):
        """Test that special Spanish regions have 0% VAT rate."""
        special_regions = {
            'CE': 'Ceuta',
            'GC': 'Las Palmas',
            'TF': 'Tenerife',
            'ML': 'Melilla',
        }

        for region_code, region_name in special_regions.items():
            with self.subTest(region=region_name, code=region_code):
                buyer = Party('ES', False, region_code)

                vat_charge = get_sale_vat_charge(
                    self.sale_date,
                    ItemType.generic_electronic_service,
                    buyer,
                    self.german_seller
                )

                self.assertEqual(vat_charge.rate, Decimal(0))
                self.assertEqual(vat_charge.action, VatChargeAction.charge)
                self.assertEqual(vat_charge.country_code, 'ES')

    def test_spanish_regular_regions_standard_vat(self):
        """Test that regular Spanish regions have standard 21% VAT rate."""
        # Madrid, Barcelona, Valencia, Andalusia
        regular_regions = ['MD', 'BC', 'VA', 'AN']

        for region_code in regular_regions:
            with self.subTest(region_code=region_code):
                buyer = Party('ES', False, region_code)

                vat_charge = get_sale_vat_charge(
                    self.sale_date,
                    ItemType.generic_electronic_service,
                    buyer,
                    self.german_seller
                )

                self.assertEqual(vat_charge.rate, Decimal(21))
                self.assertEqual(vat_charge.action, VatChargeAction.charge)
                self.assertEqual(vat_charge.country_code, 'ES')

    def test_spanish_no_region_code_standard_vat(self):
        """Test that Spanish buyers without region code get standard 21% VAT rate."""
        buyer = Party('ES', False)  # No region code

        vat_charge = get_sale_vat_charge(
            self.sale_date,
            ItemType.generic_electronic_service,
            buyer,
            self.german_seller
        )

        self.assertEqual(vat_charge.rate, Decimal(21))
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.country_code, 'ES')

    def test_spanish_ebooks_special_regions_zero_vat(self):
        """Test that ebooks in special Spanish regions have 0% VAT rate."""
        buyer = Party('ES', False, 'TF')  # Tenerife

        vat_charge = get_sale_vat_charge(
            self.sale_date,
            ItemType.ebook,
            buyer,
            self.german_seller
        )

        self.assertEqual(vat_charge.rate, Decimal(0))
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.country_code, 'ES')

    def test_spanish_ebooks_regular_regions_reduced_vat(self):
        """Test that ebooks in regular Spanish regions have 4% VAT rate."""
        buyer = Party('ES', False, 'MD')  # Madrid

        vat_charge = get_sale_vat_charge(
            self.sale_date,
            ItemType.ebook,
            buyer,
            self.german_seller
        )

        self.assertEqual(vat_charge.rate, Decimal(4))
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.country_code, 'ES')

    def test_domestic_spanish_transactions_with_regions(self):
        """Test domestic Spanish transactions with region-specific rates."""
        # Spanish seller to Spanish buyer in special region
        spanish_seller = Party('ES', True, 'MD')  # Madrid seller
        spanish_buyer = Party('ES', False, 'TF')  # Tenerife buyer

        vat_charge = get_sale_vat_charge(
            self.sale_date,
            ItemType.generic_electronic_service,
            spanish_buyer,
            spanish_seller
        )

        self.assertEqual(vat_charge.rate, Decimal(0))
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.country_code, 'ES')

    def test_spanish_seller_to_foreign_buyer_with_regions(self):
        """Test Spanish seller with region selling to foreign buyer."""
        spanish_seller = Party('ES', True, 'TF')  # Tenerife seller
        german_buyer = Party('DE', False)  # German consumer

        vat_charge = get_sale_vat_charge(
            self.sale_date,
            ItemType.generic_electronic_service,
            german_buyer,
            spanish_seller
        )

        # Should use German VAT rules, not Spanish regional rates
        self.assertEqual(vat_charge.rate, Decimal(19))
        self.assertEqual(vat_charge.action, VatChargeAction.charge)
        self.assertEqual(vat_charge.country_code, 'DE')

    def test_party_repr_with_region(self):
        """Test that Party repr includes region code when present."""
        party_with_region = Party('ES', False, 'TF')
        party_without_region = Party('ES', False)

        self.assertIn('region code = TF', repr(party_with_region))
        self.assertNotIn('region code', repr(party_without_region))
