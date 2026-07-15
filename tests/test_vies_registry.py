"""Test suite for the VIES registry's timeout configuration and handling.

These tests mock ``requests.post`` so no live calls are made against the
EU VIES SOAP endpoint.
"""

from unittest.mock import MagicMock, patch

try:
    from unittest2 import TestCase
except (ImportError):
    from unittest import TestCase

from requests import Timeout

from pyvat.registries import ViesRegistry


VALID_RESPONSE_XML = (
    u'<env:Envelope xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">'
    u'<env:Header/><env:Body>'
    u'<ns2:checkVatResponse '
    u'xmlns:ns2="urn:ec.europa.eu:taxud:vies:services:checkVat:types">'
    u'<ns2:countryCode>DK</ns2:countryCode>'
    u'<ns2:vatNumber>47458714</ns2:vatNumber>'
    u'<ns2:requestDate>2026-07-10+02:00</ns2:requestDate>'
    u'<ns2:valid>true</ns2:valid>'
    u'<ns2:name>Lego System A/S</ns2:name>'
    u'<ns2:address>Aastvej 1\n7190 Billund\n</ns2:address>'
    u'</ns2:checkVatResponse>'
    u'</env:Body></env:Envelope>'
)


def _make_response(status_code=200, content_type='text/xml', text=''):
    """Build a mock ``requests`` response object."""
    response = MagicMock()
    response.status_code = status_code
    response.headers = {'Content-Type': content_type}
    response.text = text
    return response


class ViesRegistryTimeoutTestCase(TestCase):
    """Test case for :class:`ViesRegistry` timeout configuration."""

    def test_default_timeout(self):
        """The default timeout allows for slow member state backends."""
        registry = ViesRegistry()
        self.assertEqual(registry.timeout, 30)

    def test_constructor_timeout_override(self):
        """The timeout is configurable via the constructor."""
        registry = ViesRegistry(timeout=45)
        self.assertEqual(registry.timeout, 45)

    @patch.dict('os.environ', {'PYVAT_VIES_VALIDATION_TIMEOUT_S': '60'})
    def test_env_var_timeout_override(self):
        """The timeout is configurable via PYVAT_VIES_VALIDATION_TIMEOUT_S."""
        registry = ViesRegistry()
        self.assertEqual(registry.timeout, 60.0)

    @patch.dict('os.environ', {'PYVAT_VIES_VALIDATION_TIMEOUT_S': '60'})
    def test_constructor_takes_precedence_over_env_var(self):
        """An explicit constructor timeout wins over the environment."""
        registry = ViesRegistry(timeout=45)
        self.assertEqual(registry.timeout, 45)

    @patch('pyvat.registries.requests.post')
    def test_timeout_is_passed_to_request(self, mock_post):
        """The configured timeout is used for the actual SOAP request."""
        mock_post.return_value = _make_response(text=VALID_RESPONSE_XML)

        registry = ViesRegistry(timeout=45)
        registry.check_vat_number('47458714', 'DK', False)

        self.assertEqual(mock_post.call_args.kwargs['timeout'], 45)

    def test_service_url_uses_https(self):
        """The VIES endpoint must be requested over HTTPS."""
        self.assertTrue(
            ViesRegistry.CHECK_VAT_SERVICE_URL.startswith('https://')
        )

    @patch('pyvat.registries.requests.post')
    def test_valid_vat_number_response_is_parsed(self, mock_post):
        """A valid SOAP response yields is_valid=True with business info."""
        mock_post.return_value = _make_response(text=VALID_RESPONSE_XML)

        registry = ViesRegistry()
        result = registry.check_vat_number('47458714', 'DK', False)

        self.assertTrue(result.is_valid)
        self.assertEqual(result.business_name, 'Lego System A/S')
        self.assertEqual(result.business_country_code, 'DK')

    @patch('pyvat.registries.requests.post')
    def test_timeout_is_logged_and_does_not_raise(self, mock_post):
        """A genuine timeout is still logged without raising."""
        mock_post.side_effect = Timeout('connection timed out')

        registry = ViesRegistry()
        result = registry.check_vat_number('47458714', 'DK', False)

        self.assertIsNone(result.is_valid)
        log_text = '\n'.join(result.log_lines)
        self.assertIn('timed out', log_text.lower())
