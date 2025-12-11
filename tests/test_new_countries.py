"""Test suite for new country VAT rules and registries."""

import pyvat
from pyvat.item_type import ItemType

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


