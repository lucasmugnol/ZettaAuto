# AutoMedia AI — Technical Debt Registry

## Priority Technical Debt Items

### 1. Secondary Gallery Photos Plate Masking Coordinates Order (Sprint 2.3.2 Backlog)
- **Status**: Registered / Backlog
- **Impact**: Secondary gallery photos in Stage 8 currently undergo `image_processor.process_image` (resize/contain) followed by `apply_plate_cover` using original source image coordinates.
- **Resolution Plan**: Refactor Stage 8 to follow the exact Fail-Closed Plate Cover execution order introduced for Cover photos in Sprint 2.3.2 (applying plate cover on a temporary copy of original source image prior to image scaling).
