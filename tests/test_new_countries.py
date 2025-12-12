"""Test suite for new country VAT rules and registries."""

import datetime
import pyvat
from pyvat import get_sale_vat_charge, Party, VatChargeAction
from pyvat.item_type import ItemType
from decimal import Decimal

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
            ('CA', 'Canada', 0),
            ('NO', 'Norway', 25),
            ('MC', 'Monaco', 20),
            ('RE', 'Réunion (DOM)', 8.5),
            ('GP', 'Guadeloupe (DOM)', 8.5),
            ('MQ', 'Martinique (DOM)', 8.5),
        ]

        for code, name, expected_rate in test_cases:
            with self.subTest(country=name, code=code):
                rules = pyvat.vat_rules.VAT_RULES[code]
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
        # Note: MC, RE, GP, MQ are now EU countries and use VIES registry

        for code, name, expected_valid, description in test_cases:
            with self.subTest(country=name, code=code):
                registry = pyvat.VAT_REGISTRIES[code]
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
        """
        test_cases = [
            # (country_code, country_name, expected_vat_rate, description)
            ('EG', 'Egypt', Decimal('14'), 'B2B exempt - but VAT still charged'),
            ('CH', 'Switzerland', Decimal('8.1'), 'B2B not exempt - VAT charged'),
            ('CA', 'Canada', Decimal('0'), 'B2B exempt - but 0% VAT charged'),
            ('NO', 'Norway', Decimal('25'), 'B2B not exempt - VAT charged'),
        ]

        for country_code, country_name, expected_rate, description in test_cases:
            with self.subTest(country=country_name, code=country_code):
                # Test B2B transaction from EU seller to non-EU buyer
                vat_charge = get_sale_vat_charge(
                    datetime.date(2024, 1, 1),
                    ItemType.generic_electronic_service,
                    Party(country_code=country_code, is_business=True),  # Non-EU B2B buyer
                    Party(country_code='FR', is_business=True)  # EU seller
                )

                # Should charge VAT (not reverse charge or no charge)
                self.assertEqual(
                    vat_charge.action,
                    VatChargeAction.charge,
                    f"{country_name} B2B should be charged VAT (not reverse charge) - {description}"
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

