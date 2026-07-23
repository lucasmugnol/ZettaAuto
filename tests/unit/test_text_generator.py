"""Unit tests for TextGenerator without hallucinating unconfirmed data."""

from automedia.core.models import VehicleData, BrandConfig
from automedia.providers.deterministic_text_provider import DeterministicTextProvider
from automedia.modules.text_generator import TextGenerator


def test_text_generator_omits_missing_fields_without_hallucinating():
    vdata = VehicleData(
        manufacturer="Honda",
        model="Civic Touring",
        year=2021,
        price="R$ 135.000",
        description="Carro de garagem em excelente estado.",
        optional_features=["Teto solar elétrico", "Banco de couro"]
    )
    bcfg = BrandConfig(
        company_name="Top Car Auto",
        contact="(11) 98888-7777",
        cta="Venha fazer um test drive!"
    )

    provider = DeterministicTextProvider()
    generator = TextGenerator(provider)
    title, desc = generator.generate(vdata, bcfg)

    assert title == "Honda Civic Touring 2021 — R$ 135.000"
    assert "Honda Civic Touring (2021)" in desc
    assert "Preço: R$ 135.000" in desc
    assert "Carro de garagem em excelente estado." in desc
    assert "• Teto solar elétrico" in desc
    assert "Top Car Auto" in desc
    assert "(11) 98888-7777" in desc
    assert "Venha fazer um test drive!" in desc

    # Strict check: ensure unconfirmed fields like "Câmbio", "Garantia", "Manual", "Revisões" are NOT hallucinated
    forbidden_terms = ["câmbio", "garantia", "procedência", "financiamento", "laudo"]
    for term in forbidden_terms:
        assert term not in desc.lower()


def test_text_generator_handles_minimal_fields():
    vdata = VehicleData(
        manufacturer="Fiat",
        model="Uno Mille",
        year=2010,
        price="R$ 20.000"
    )
    bcfg = BrandConfig(company_name="AutoExpress")

    generator = TextGenerator(DeterministicTextProvider())
    title, desc = generator.generate(vdata, bcfg)

    assert title == "Fiat Uno Mille 2010 — R$ 20.000"
    assert "Fiat Uno Mille (2010)" in desc
    assert "AutoExpress" in desc
    assert "Opcionais" not in desc
