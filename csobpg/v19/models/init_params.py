from typing import List, Optional, Dict

from ..signature import SignedModel


class InitPramsGoogle(SignedModel):
    allowed_card_auth_methods: List[str]
    allowed_card_networks: List[str]
    api_version: int
    api_version_minor: int
    assurance_details_required: bool
    billing_address_parameters_format: str
    billing_address_required: bool
    country_code: str
    environment: str
    gateway: str
    gateway_merchant_id: str
    googlepay_merchant_id: str
    merchant_name: str
    payment_method_type: str
    tokenization_specification_type: str
    total_price_status: str

    def __init__(self):
        self.allowed_card_auth_methods: List[str]
        self.allowed_card_networks: List[str]
        self.api_version: int
        self.api_version_minor: int
        self.assurance_details_required: bool
        self.billing_address_parameters_format: str
        self.billing_address_required: bool
        self.country_code: str
        self.environment: str
        self.gateway: str
        self.gateway_merchant_id: str
        self.googlepay_merchant_id: str
        self.merchant_name: str
        self.payment_method_type: str
        self.tokenization_specification_type: str
        self.total_price_status: str

    def _get_params_sequence(self):
        return (
            "|".join(self.allowed_card_auth_methods),
            "|".join(self.allowed_card_networks),
            self.api_version,
            self.api_version_minor,
            self.assurance_details_required,
            self.billing_address_parameters_format,
            self.billing_address_required,
            self.country_code,
            self.environment,
            self.gateway,
            self.gateway_merchant_id,
            self.googlepay_merchant_id,
            self.merchant_name,
            self.payment_method_type,
            self.tokenization_specification_type,
            self.total_price_status,
        )


class InitParamsApple(SignedModel):
    country_code: str
    supported_networks = Dict[str, str]
    merchant_capabilities = Dict[str, str]

    def __init__(
        self,
        country_code: Optional[str] = None,
        supported_networks: Optional[Dict[str, str]] = None,
        merchant_capabilities: Optional[Dict[str, str]] = None,
    ) -> None:
        self.country_code = country_code
        self.supported_networks = supported_networks
        self.merchant_capabilities = merchant_capabilities

    def _get_params_sequence(self) -> tuple:
        return (
            self.country_code,
            self.supported_networks,
            self.merchant_capabilities,
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"countryCode='{self.country_code}', "
            f"supportedNetworks={self.supported_networks}, "
            f"merchantCapabilities={self.merchant_capabilities}"
            ")"
        )
