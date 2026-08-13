"""Test suite for the HMRC registry's VAT number check handling.

These tests mock ``requests.get`` so no live calls are made against the
HMRC API. Each test pre-seeds ``access_token`` on the registry instance so
that the authentication path (which itself makes an HTTP request) is
skipped and only the ``check_vat_number`` response-handling logic under
test is exercised.
"""

from unittest.mock import MagicMock, patch

try:
    from unittest2 import TestCase
except (ImportError):
    from unittest import TestCase

from requests import Timeout

from pyvat.exceptions import ServerError
from pyvat.registries import HMRCRegistry


def _make_response(status_code, content_type='application/json', text='', json_data=None):
    """Build a mock ``requests`` response object."""
    response = MagicMock()
    response.status_code = status_code
    response.headers = {'Content-Type': content_type}
    response.text = text
    if json_data is not None:
        response.json.return_value = json_data
    return response


class HMRCRegistryTestCase(TestCase):
    """Test case for :class:`HMRCRegistry`."""

    def setUp(self):
        self.registry = HMRCRegistry()
        # Skip the _authenticate() call inside check_vat_number.
        self.registry.access_token = 'test-token'

    @patch('pyvat.registries.requests.get')
    def test_404_not_found_is_not_reported_as_outage(self, mock_get):
        """A 404 means the VAT number was not found, not a service outage."""
        mock_get.return_value = _make_response(
            404, text='{"code": "NOT_FOUND"}'
        )

        result = self.registry.check_vat_number('123456789', 'GB', False)

        self.assertFalse(result.is_valid)
        log_text = '\n'.join(result.log_lines)
        self.assertNotIn('nondeterministic', log_text)
        self.assertNotIn('ServerError', log_text)
        self.assertNotIn('Exception', log_text)
        self.assertIn('not found', log_text.lower())

    @patch('pyvat.registries.requests.get')
    def test_400_is_not_reported_as_outage(self, mock_get):
        """A 400 is an authoritative bad request, not a service outage."""
        mock_get.return_value = _make_response(
            400, text='{"code": "INVALID_VAT_NUMBER"}'
        )

        result = self.registry.check_vat_number('123456789', 'GB', False)

        self.assertFalse(result.is_valid)
        log_text = '\n'.join(result.log_lines)
        self.assertNotIn('nondeterministic', log_text)

    @patch('pyvat.registries.requests.get')
    def test_500_raises_server_error(self, mock_get):
        """A 500 (genuine outage) must raise ServerError."""
        mock_get.return_value = _make_response(
            500, text='Internal Server Error'
        )

        with self.assertRaises(ServerError):
            self.registry.check_vat_number('123456789', 'GB', False)

    @patch('pyvat.registries.requests.get')
    def test_200_with_valid_target_returns_valid_result(self, mock_get):
        """A 200 response with a target payload is a valid VAT number."""
        json_data = {
            'target': {
                'name': 'Credite Sberger Donal Inc.',
                'vatNumber': '553557881',
                'address': {
                    'line1': '131B Barton Hamlet',
                    'postcode': 'SW97 5CK',
                    'countryCode': 'GB',
                },
            },
            'processingDate': '2022-09-29T12:08:48+01:00',
        }
        mock_get.return_value = _make_response(
            200, text='irrelevant', json_data=json_data
        )

        result = self.registry.check_vat_number('553557881', 'GB', False)

        self.assertTrue(result.is_valid)
        self.assertEqual(result.business_name, 'Credite Sberger Donal Inc.')
        self.assertIn('131B Barton Hamlet', result.business_address)

    @patch('pyvat.registries.requests.get')
    def test_malformed_content_type_raises_server_error(self, mock_get):
        """A 200 response with a non-JSON content type is a service outage."""
        mock_get.return_value = _make_response(
            200, content_type='text/html', text='<html>not json</html>'
        )

        with self.assertRaises(ServerError):
            self.registry.check_vat_number('123456789', 'GB', False)

    def test_default_timeout(self):
        """The default timeout matches the documented class default."""
        self.assertEqual(self.registry.timeout, 12)

    def test_constructor_timeout_override(self):
        """The timeout is configurable via the constructor."""
        registry = HMRCRegistry(timeout=30)
        self.assertEqual(registry.timeout, 30)

    @patch.dict('os.environ', {'PYVAT_HMRC_VALIDATION_TIMEOUT_S': '25'})
    def test_env_var_timeout_override(self):
        """The timeout is configurable via PYVAT_HMRC_VALIDATION_TIMEOUT_S."""
        registry = HMRCRegistry()
        self.assertEqual(registry.timeout, 25.0)

    @patch('pyvat.registries.requests.get')
    def test_timeout_is_passed_to_request(self, mock_get):
        """The configured timeout is used for the lookup request."""
        mock_get.return_value = _make_response(
            404, text='{"code": "NOT_FOUND"}'
        )

        registry = HMRCRegistry(timeout=30)
        registry.access_token = 'test-token'
        registry.check_vat_number('123456789', 'GB', False)

        self.assertEqual(mock_get.call_args.kwargs['timeout'], 30)

    @patch('pyvat.registries.requests.get')
    def test_timeout_raises_server_error(self, mock_get):
        """A request timeout must raise ServerError so outage detection works."""
        mock_get.side_effect = Timeout('connection timed out')

        with self.assertRaises(ServerError):
            self.registry.check_vat_number('123456789', 'GB', False)

    @patch('pyvat.registries.requests.get')
    def test_generic_request_exception_raises_server_error(self, mock_get):
        """An unexpected exception during the request must raise ServerError."""
        mock_get.side_effect = ValueError('boom')

        with self.assertRaises(ServerError):
            self.registry.check_vat_number('123456789', 'GB', False)
