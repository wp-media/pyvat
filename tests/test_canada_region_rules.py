"""Tests for CanadaRegionRules."""

from decimal import Decimal

try:
    from unittest2 import TestCase
except (ImportError, AttributeError):
    from unittest import TestCase

from pyvat.region_rules import CanadaRegionRules


class CanadaRegionRulesGetRateTestCase(TestCase):
    """Tests for CanadaRegionRules.get_rate()."""

    def setUp(self):
        self.rules = CanadaRegionRules()

    def test_returns_ontario_fallback_when_no_postal_code(self):
        self.assertEqual(self.rules.get_rate(None), Decimal('13'))

    def test_returns_ontario_fallback_for_empty_string(self):
        self.assertEqual(self.rules.get_rate(''), Decimal('13'))

    def test_returns_ontario_fallback_for_unknown_prefix(self):
        # 'Z' is not a valid Canadian postal prefix
        self.assertEqual(self.rules.get_rate('Z1A 0A0'), Decimal('13'))

    def test_rate_by_province(self):
        test_cases = [
            ('A1A 5T9', Decimal('15'), 'Newfoundland and Labrador (HST)'),
            ('B3H 1Y2', Decimal('14'), 'Nova Scotia (HST)'),
            ('C1A 4P3', Decimal('15'), 'Prince Edward Island (HST)'),
            ('E2L 4H8', Decimal('15'), 'New Brunswick (HST)'),
            ('G1A 0A2', Decimal('5'),  'Quebec (GST only — not registered for QST)'),
            ('H1A 0A1', Decimal('5'),  'Quebec (GST only — not registered for QST)'),
            ('J1A 1A1', Decimal('5'),  'Quebec (GST only — not registered for QST)'),
            ('K1A 0B1', Decimal('13'), 'Ontario (HST)'),
            ('L5B 4M7', Decimal('13'), 'Ontario (HST)'),
            ('M5V 3L9', Decimal('13'), 'Ontario (HST)'),
            ('N2L 3G1', Decimal('13'), 'Ontario (HST)'),
            ('P7B 5E1', Decimal('13'), 'Ontario (HST)'),
            ('R2C 0A1', Decimal('5'),  'Manitoba (GST only — not registered for RST)'),
            ('S7K 1A1', Decimal('11'), 'Saskatchewan (GST + PST)'),
            ('T5J 0N3', Decimal('5'),  'Alberta (GST only)'),
            ('V6B 4N6', Decimal('12'), 'British Columbia (GST + PST)'),
            ('X0A 0H0', Decimal('5'),  'Northwest Territories and Nunavut (GST only)'),
            ('Y1A 0A1', Decimal('5'),  'Yukon (GST only)'),
        ]

        for postal_code, expected_rate, description in test_cases:
            with self.subTest(postal_code=postal_code, description=description):
                self.assertEqual(self.rules.get_rate(postal_code), expected_rate)

    def test_lowercase_postal_code_is_normalised(self):
        self.assertEqual(self.rules.get_rate('m5v 3l9'), Decimal('13'))

    def test_postal_code_with_leading_whitespace_is_normalised(self):
        self.assertEqual(self.rules.get_rate('  M5V 3L9'), Decimal('13'))

    def test_prefix_only_is_accepted(self):
        self.assertEqual(self.rules.get_rate('V'), Decimal('12'))


class CanadaRegionRulesGetRegionTestCase(TestCase):
    """Tests for CanadaRegionRules.get_region()."""

    def setUp(self):
        self.rules = CanadaRegionRules()

    def test_returns_none_when_no_postal_code(self):
        self.assertIsNone(self.rules.get_region(None))

    def test_returns_none_for_empty_string(self):
        self.assertIsNone(self.rules.get_region(''))

    def test_returns_none_for_unknown_prefix(self):
        self.assertIsNone(self.rules.get_region('Z1A 0A0'))

    def test_province_names(self):
        test_cases = [
            ('A', 'Newfoundland and Labrador'),
            ('B', 'Nova Scotia'),
            ('C', 'Prince Edward Island'),
            ('E', 'New Brunswick'),
            ('G', 'Quebec'),
            ('H', 'Quebec'),
            ('J', 'Quebec'),
            ('K', 'Ontario'),
            ('L', 'Ontario'),
            ('M', 'Ontario'),
            ('N', 'Ontario'),
            ('P', 'Ontario'),
            ('R', 'Manitoba'),
            ('S', 'Saskatchewan'),
            ('T', 'Alberta'),
            ('V', 'British Columbia'),
            ('X', 'Northwest Territories and Nunavut'),
            ('Y', 'Yukon'),
        ]

        for prefix, expected_province in test_cases:
            with self.subTest(prefix=prefix):
                region = self.rules.get_region(prefix)
                self.assertEqual(region.province, expected_province)

    def test_prefix_field_matches_lookup_key(self):
        region = self.rules.get_region('M5V 3L9')
        self.assertEqual(region.prefix, 'M')

    def test_rate_field_matches_get_rate(self):
        for postal_code in ('A', 'B', 'C', 'E', 'G', 'K', 'R', 'S', 'T', 'V', 'X', 'Y'):
            with self.subTest(postal_code=postal_code):
                region = self.rules.get_region(postal_code)
                self.assertEqual(region.rate, self.rules.get_rate(postal_code))

    def test_lowercase_postal_code_is_normalised(self):
        region = self.rules.get_region('v6b 4n6')
        self.assertIsNotNone(region)
        self.assertEqual(region.province, 'British Columbia')


class CanadaRegionRulesTaxTypesTestCase(TestCase):
    """Tests for tax_types on ProvinceRate."""

    def setUp(self):
        self.rules = CanadaRegionRules()

    def test_hst_provinces_have_single_hst_tax_type(self):
        hst_prefixes = ('A', 'B', 'C', 'E', 'K', 'L', 'M', 'N', 'P')

        for prefix in hst_prefixes:
            with self.subTest(prefix=prefix):
                region = self.rules.get_region(prefix)
                self.assertEqual(region.tax_types, (CanadaRegionRules.HST,))

    def test_gst_pst_provinces_have_two_tax_types(self):
        for prefix in ('S', 'V'):
            with self.subTest(prefix=prefix):
                region = self.rules.get_region(prefix)
                self.assertIn(CanadaRegionRules.GST, region.tax_types)
                self.assertIn(CanadaRegionRules.PST, region.tax_types)

    def test_unregistered_and_gst_only_provinces_have_single_gst_tax_type(self):
        # Quebec (QST), Manitoba (RST), Alberta, NWT/Nunavut, Yukon
        gst_only_prefixes = ('G', 'H', 'J', 'R', 'T', 'X', 'Y')

        for prefix in gst_only_prefixes:
            with self.subTest(prefix=prefix):
                region = self.rules.get_region(prefix)
                self.assertEqual(region.tax_types, (CanadaRegionRules.GST,))


class CanadaRegionRulesConstantsTestCase(TestCase):
    """Tests for tax-type constants on CanadaRegionRules."""

    def test_constant_values(self):
        self.assertEqual(CanadaRegionRules.GST, 'GST')
        self.assertEqual(CanadaRegionRules.HST, 'HST')
        self.assertEqual(CanadaRegionRules.PST, 'PST')
        self.assertEqual(CanadaRegionRules.QST, 'QST')
        self.assertEqual(CanadaRegionRules.RST, 'RST')

    def test_default_rate_is_ontario(self):
        self.assertEqual(CanadaRegionRules.DEFAULT_RATE, Decimal('13'))

    def test_all_prefixes_are_covered(self):
        # Valid Canada Post first-letter prefixes (D, F, I, O, Q, U, W, Z are not assigned)
        expected_prefixes = {'A', 'B', 'C', 'E', 'G', 'H', 'J', 'K', 'L', 'M',
                             'N', 'P', 'R', 'S', 'T', 'V', 'X', 'Y'}
        self.assertEqual(set(CanadaRegionRules.PROVINCE_RATES.keys()), expected_prefixes)
