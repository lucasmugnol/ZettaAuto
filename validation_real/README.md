# Validation Real Dataset Directory

This directory contains real vehicle photograph datasets and human ground truth annotations.

## Directory Structure

```text
validation_real/
  vehicle_01/
    images/
      IMG_001.jpg
      IMG_002.jpg
      ...
    ground_truth.json
```

## Privacy & Version Control Policy

Private/customer photographs **MUST NOT** be committed to Git.
The root `.gitignore` ignores all contents of `validation_real/` except `README.md` and `ground_truth.example.json`.
