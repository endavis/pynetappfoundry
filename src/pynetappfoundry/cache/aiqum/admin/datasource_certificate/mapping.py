"""AiqumCertificateResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.admin.datasource_certificate.model import AiqumCertificateResponse

AIQUMCERTIFICATERESPONSE_MAPPING = TypeMapping(
    name="AiqumCertificateResponse",
    model_class=AiqumCertificateResponse,
    api_endpoint="/admin/datasource-certificate",
    api_type="aiqum",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="detail_certificate_string",
        ),
        FieldMapping(
            cache_attr="fingerprint.md5",
        ),
        FieldMapping(
            cache_attr="fingerprint.sha1",
        ),
        FieldMapping(
            cache_attr="is_self_signed",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_valid",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_valid_hostname",
            default=False,
        ),
        FieldMapping(
            cache_attr="issued_to",
        ),
        FieldMapping(
            cache_attr="issuer",
        ),
        FieldMapping(
            cache_attr="pem_formatted_string",
        ),
        FieldMapping(
            cache_attr="valid_from",
        ),
        FieldMapping(
            cache_attr="valid_to",
        ),
    ),
)

model_registry.register_mapping("AiqumCertificateResponse", AIQUMCERTIFICATERESPONSE_MAPPING)
