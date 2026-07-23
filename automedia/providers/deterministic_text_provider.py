"""Deterministic text provider implementation."""

from typing import Tuple
from automedia.core.interfaces import ITextProvider
from automedia.core.models import VehicleData, BrandConfig


class DeterministicTextProvider(ITextProvider):
    def generate_ad_text(
        self, vehicle_data: VehicleData, brand_config: BrandConfig
    ) -> Tuple[str, str]:
        # Title: {manufacturer} {model} {year} — {price}
        title = f"{vehicle_data.manufacturer} {vehicle_data.model} {vehicle_data.year} — {vehicle_data.price}".strip()

        # Description: strictly confirmed fields only
        lines = [
            f"🚘 {vehicle_data.manufacturer} {vehicle_data.model} ({vehicle_data.year})",
            f"💰 Preço: {vehicle_data.price}",
            ""
        ]

        if vehicle_data.description:
            lines.append("📝 Sobre o veículo:")
            lines.append(vehicle_data.description.strip())
            lines.append("")

        if vehicle_data.optional_features:
            lines.append("✨ Destaques e Opcionais:")
            for feature in vehicle_data.optional_features:
                lines.append(f" • {feature.strip()}")
            lines.append("")

        lines.append("📍 Informações da Loja:")
        lines.append(f"🏢 {brand_config.company_name}")
        if brand_config.contact:
            lines.append(f"📞 Contato: {brand_config.contact}")
        if brand_config.cta:
            lines.append(f"💬 {brand_config.cta}")

        description = "\n".join(lines).strip()
        return title, description
