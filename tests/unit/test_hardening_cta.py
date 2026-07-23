"""Unit tests for CTA non-invention rules."""

from automedia.core.models import VehicleData, BrandConfig
from automedia.providers.deterministic_text_provider import DeterministicTextProvider


def test_absent_cta_omits_cta_line_and_forbidden_words():
    vdata = VehicleData(
        manufacturer="Chevrolet",
        model="Onix Premier",
        year=2023,
        price="R$ 89.900"
    )
    bcfg = BrandConfig(
        company_name="Safe Dealer",
        cta=""  # Empty CTA
    )

    provider = DeterministicTextProvider()
    title, desc = provider.generate_ad_text(vdata, bcfg)

    forbidden_terms = ["financiamento", "garantia", "entrada", "parcelas", "consulte"]
    for term in forbidden_terms:
        assert term not in desc.lower()

    # When CTA is explicit
    bcfg_with_cta = BrandConfig(company_name="Safe Dealer", cta="Fale conosco no WhatsApp!")
    _, desc_with_cta = provider.generate_ad_text(vdata, bcfg_with_cta)
    assert "Fale conosco no WhatsApp!" in desc_with_cta
