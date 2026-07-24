"""Vision models and dataclasses for Multimodal Vision Provider (Sprint 2.3)."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from automedia.core.models import PhotoCategory, MacroCategory


@dataclass
class MultimodalAnalysisResult:
    category: str = PhotoCategory.UNKNOWN
    macro_category: str = MacroCategory.UNKNOWN
    confidence: float = 0.0
    suitable_for_cover: bool = False
    cover_score: float = 0.0
    quality_status: str = "GOOD"  # "GOOD", "WARNING", "BAD"
    visual_issues: List[str] = field(default_factory=list)
    composition_score: float = 0.0
    framing_score: float = 0.0
    vehicle_visibility: float = 0.0
    content_bbox_estimate: Optional[Dict[str, int]] = None
    plate_visible: bool = False
    plate_bbox: Optional[Dict[str, int]] = None
    reasoning_summary: str = ""

    # Metadata & Auditing
    provider_used: str = "heuristic"
    model_used: str = "local_heuristic"
    prompt_version: str = "v1.0.0"
    inference_status: str = "SUCCESS"  # "SUCCESS", "FALLBACK_HEURISTIC", "CACHE_HIT", "FAILED"
    fallback_used: bool = False
    fallback_reason: Optional[str] = None
    latency_ms: float = 0.0
    estimated_cost_usd: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "macro_category": self.macro_category or MacroCategory.get_macro(self.category),
            "confidence": round(self.confidence, 2),
            "suitable_for_cover": self.suitable_for_cover,
            "cover_score": round(self.cover_score, 2),
            "quality_status": self.quality_status,
            "visual_issues": self.visual_issues,
            "composition_score": round(self.composition_score, 2),
            "framing_score": round(self.framing_score, 2),
            "vehicle_visibility": round(self.vehicle_visibility, 2),
            "content_bbox_estimate": self.content_bbox_estimate,
            "plate_visible": self.plate_visible,
            "plate_bbox": self.plate_bbox,
            "reasoning_summary": self.reasoning_summary,
            "metadata": {
                "provider_used": self.provider_used,
                "model_used": self.model_used,
                "prompt_version": self.prompt_version,
                "inference_status": self.inference_status,
                "fallback_used": self.fallback_used,
                "fallback_reason": self.fallback_reason,
                "latency_ms": round(self.latency_ms, 2),
                "estimated_cost_usd": round(self.estimated_cost_usd, 6)
            }
        }
