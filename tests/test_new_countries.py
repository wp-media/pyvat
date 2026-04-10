"""Test suite for new country VAT rules and registries."""

import datetime
from decimal import Decimal
from pyvat import get_sale_vat_charge, Party, VatChargeAction, VAT_REGISTRIES
from pyvat.item_type import ItemType
from pyvat.vat_rules import VAT_RULES

try:
    from unittest2 import TestCase
except (ImportError, AttributeError):
    from unittest import TestCase


class NewCountriesVatRulesTestCase(TestCase):
    """Test case for new countries VAT rules."""

    def test_vat_rates(self):
        """Test that VAT rates are correct for all new countries."""
        test_cases = [
            ('EG', 'Egypt', 14),
            ('CH', 'Switzerland', 8.1),
            ('CA', 'Canada', 13),  # No postal code → Ontario fallback (13%)
            ('NO', 'Norway', 25),
            ('MC', 'Monaco', 20),
            ('RE', 'Réunion (DOM)', 8.5),
            ('GP', 'Guadeloupe (DOM)', 8.5),
            ('MQ', 'Martinique (DOM)', 8.5),
        ]

        for code, name, expected_rate in test_cases:
            with self.subTest(country=name, code=code):
                rules = VAT_RULES[code]
                rate = rules.get_vat_rate(ItemType.generic_electronic_service)
                self.assertEqual(
                    float(rate),
                    expected_rate,
                    f"{name} ({code}) should have {expected_rate}% VAT"
                )


class NewCountriesRegistriesTestCase(TestCase):
    """Test case for new countries registries (B2B exemption)."""

    def test_b2b_exemption(self):
        """Test that B2B exemption rules are correctly implemented for non-EU countries."""
        test_cases = [
            ('EG', 'Egypt', True, 'B2B exempt'),
            ('CH', 'Switzerland', False, 'B2B not exempt'),
            ('CA', 'Canada', True, 'B2B exempt'),
            ('NO', 'Norway', False, 'B2B not exempt'),
        ]
        # Note: Only MC (Monaco) is treated as an EU country for VAT purposes and uses the VIES registry.
        # RE (Réunion), GP (Guadeloupe), and MQ (Martinique) are French DOM territories: they use VIES for VAT number validation,
        # but are outside the EU VAT territory.

        for code, name, expected_valid, description in test_cases:
            with self.subTest(country=name, code=code):
                registry = VAT_REGISTRIES[code]
                result = registry.check_vat_number('123456789', code, False)
                self.assertEqual(
                    result.is_valid,
                    expected_valid,
                    f"{name} ({code}) registry should return is_valid={expected_valid} ({description})"
                )


class NonEuB2BVatChargeTestCase(TestCase):
    """Test case for non-EU B2B VAT charges."""

    def test_non_eu_b2b_vat_charges(self):
        """Test that non-EU B2B customers are charged correct VAT rates.

        Unlike EU B2B transactions which use reverse charge, these non-EU countries
        require VAT to be charged per government mandate, regardless of B2B status.

        Exception: Egypt B2B transactions are now exempt (0% VAT).
        """
        test_cases = [
            # (country_code, country_name, expected_vat_rate, expected_action, description)
            ('EG', 'Egypt', Decimal('0'), VatChargeAction.no_charge, 'B2B exempt - no VAT charged'),
            ('CH', 'Switzerland', Decimal('8.1'), VatChargeAction.charge, 'B2B not exempt - VAT charged'),
            ('CA', 'Canada', Decimal('13'), VatChargeAction.charge, 'B2B not exempt - Ontario fallback rate (13%) applied'),
            ('NO', 'Norway', Decimal('25'), VatChargeAction.charge, 'B2B not exempt - VAT charged'),
        ]

        for country_code, country_name, expected_rate, expected_action, description in test_cases:
            with self.subTest(country=country_name, code=country_code):
                # Test B2B transaction from EU seller to non-EU buyer
                vat_charge = get_sale_vat_charge(
                    datetime.date(2024, 1, 1),
                    ItemType.generic_electronic_service,
                    Party(country_code=country_code, is_business=True),  # Non-EU B2B buyer
                    Party(country_code='FR', is_business=True)  # EU seller
                )

                # Check expected action
                self.assertEqual(
                    vat_charge.action,
                    expected_action,
                    f"{country_name} B2B should have action {expected_action} - {description}"
                )

                # Should charge correct VAT rate
                self.assertEqual(
                    vat_charge.rate,
                    expected_rate,
                    f"{country_name} B2B should be charged {expected_rate}% VAT - {description}"
                )

                # Should charge in buyer's country
                self.assertEqual(
                    vat_charge.country_code,
                    country_code,
                    f"VAT should be charged in {country_name} ({country_code})"
                )


class CanadaProvinceVatRatesTestCase(TestCase):
    """Test Canada province-specific VAT rates based on postal code prefix."""

    def test_province_rates(self):
        """Test that the correct VAT rate is returned for each province."""
        rules = VAT_RULES['CA']
        item_type = ItemType.generic_electronic_service

        test_cases = [
            # (postal_code, province, expected_rate, note)
            (None,    'No postal code (Ontario fallback)', Decimal('13'),   'fallback'),
            ('A1A 5T9', 'Newfoundland and Labrador',      Decimal('15'),   'HST'),
            ('B3H 1Y2', 'Nova Scotia',                    Decimal('14'),   'HST'),
            ('C1A 4P3', 'Prince Edward Island',           Decimal('15'),   'HST'),
            ('E2L 4H8', 'New Brunswick',                  Decimal('15'),   'HST'),
            ('G1A 0A2', 'Quebec',                         Decimal('5'),    'not registered → GST only'),
            ('H1A 0A1', 'Quebec',                         Decimal('5'),    'not registered → GST only'),
            ('J1A 1A1', 'Quebec',                         Decimal('5'),    'not registered → GST only'),
            ('K1A 0B1', 'Ontario',                        Decimal('13'),   'HST'),
            ('L5B 4M7', 'Ontario',                        Decimal('13'),   'HST'),
            ('M5V 3L9', 'Ontario',                        Decimal('13'),   'HST'),
            ('N2L 3G1', 'Ontario',                        Decimal('13'),   'HST'),
            ('P7B 5E1', 'Ontario',                        Decimal('13'),   'HST'),
            ('R2C 0A1', 'Manitoba',                       Decimal('5'),    'not registered → GST only'),
            ('S7K 1A1', 'Saskatchewan',                   Decimal('11'),   'GST + PST (registered)'),
            ('T5J 0N3', 'Alberta',                        Decimal('5'),    'GST only'),
            ('V6B 4N6', 'British Columbia',               Decimal('12'),   'GST + PST (registered)'),
            ('X0A 0H0', 'Northwest Territories/Nunavut',  Decimal('5'),    'GST only'),
            ('Y1A 0A1', 'Yukon',                          Decimal('5'),    'GST only'),
        ]

        for postal_code, province, expected_rate, note in test_cases:
            with self.subTest(province=province, postal_code=postal_code):
                rate = rules.get_vat_rate(item_type, postal_code)
                self.assertEqual(
                    rate,
                    expected_rate,
                    f"{province} ({postal_code!r}) should be {expected_rate}% — {note}"
                )

    def test_b2b_no_exemption(self):
        """Test that B2B transactions are charged the same rate as B2C."""
        test_cases = [
            ('V6B 4N6', Decimal('12'),  'British Columbia'),
            ('S7K 1A1', Decimal('11'),  'Saskatchewan'),
            ('K1A 0B1', Decimal('13'),  'Ontario'),
            ('A1A 5T9', Decimal('15'),  'Newfoundland and Labrador'),
            ('G1A 0A2', Decimal('5'),   'Quebec (not registered)'),
            ('R2C 0A1', Decimal('5'),   'Manitoba (not registered)'),
            (None,      Decimal('13'),  'No postal code (Ontario fallback)'),
        ]

        for postal_code, expected_rate, province in test_cases:
            with self.subTest(province=province):
                vat_charge = get_sale_vat_charge(
                    datetime.date(2024, 1, 1),
                    ItemType.generic_electronic_service,
                    Party(country_code='CA', is_business=True),
                    Party(country_code='FR', is_business=True),
                    postal_code=postal_code,
                )
                self.assertEqual(
                    vat_charge.action,
                    VatChargeAction.charge,
                    f"{province}: B2B should still be charged VAT"
                )
                self.assertEqual(
                    vat_charge.rate,
                    expected_rate,
                    f"{province}: B2B rate should match B2C rate ({expected_rate}%)"
                )
