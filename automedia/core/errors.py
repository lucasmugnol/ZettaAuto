"""Custom domain exceptions for AutoMedia AI pipeline."""


class AutomediaError(Exception):
    """Base exception for all AutoMedia domain errors."""
    pass


class ConfigurationError(AutomediaError):
    """Raised when configuration files or values are missing or invalid."""
    pass


class InvalidInputError(AutomediaError):
    """Raised when input paths, folders or parameters are invalid."""
    pass


class EmptyBatchError(AutomediaError):
    """Raised when no usable images are found in the input batch."""
    pass


class CorruptedImageError(AutomediaError):
    """Raised when an image file cannot be opened or decoded."""
    pass


class ProcessingError(AutomediaError):
    """Raised when image manipulation or processing fails."""
    pass


class CoverFailureError(AutomediaError):
    """Raised when the primary cover image generation or selection fails."""
    pass


class ExportError(AutomediaError):
    """Raised when consolidating, zipping or saving export artifacts fails."""
    pass
