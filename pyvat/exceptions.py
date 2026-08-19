class ServerError(Exception):
    """Raised by a registry when it cannot authoritatively check a VAT number.

    Every registry (:class:`~pyvat.registries.ViesRegistry`,
    :class:`~pyvat.registries.HMRCRegistry`) raises this same exception for
    any outage-like condition: a request timeout, a transport-level
    exception, an HTTP 500 / SOAP fault, or an unexpected response format.
    Callers should catch it to distinguish "the service is unavailable"
    from an authoritative ``is_valid=False`` result, instead of matching on
    ``VatNumberCheckResult.log_lines`` text, which is not part of the API
    contract and may change between releases.
    """

    def __init__(self, fault_code):
        super(ServerError, self).__init__("ServerError: {}".format(fault_code))
        self.fault_code = fault_code
