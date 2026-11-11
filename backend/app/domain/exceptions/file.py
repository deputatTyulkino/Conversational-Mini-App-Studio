from collections.abc import Iterable

from .base import (
    BusinessRuleViolationError,
    DomainError,
    DomainValidationError,
    NotFoundError,
)


class FileNameMissingError(DomainValidationError):
    code = "file_name_missing"
    default_message = "File name is missing"


class FileEmptyError(DomainValidationError):
    code = "file_empty"
    default_message = "File is empty"


class FileExtensionNotAllowedError(DomainValidationError):
    code = "file_extension_not_allowed"

    def __init__(self, extension: str, allowed: Iterable[str]) -> None:
        super().__init__(
            f"File extension '{extension or '(none)'}' is not allowed",
            extension=extension,
            allowed=sorted(allowed),
        )


class FileContentTypeNotAllowedError(DomainValidationError):
    code = "file_content_type_not_allowed"

    def __init__(self, content_type: str, allowed: Iterable[str]) -> None:
        super().__init__(
            f"Content type '{content_type or '(none)'}' is not allowed",
            content_type=content_type,
            allowed=sorted(allowed),
        )


class FileTooLargeError(DomainValidationError):
    code = "file_too_large"

    def __init__(self, max_size: int) -> None:
        super().__init__(
            f"File must not exceed {max_size} bytes",
            max_size=max_size,
        )


class TooManyFilesError(BusinessRuleViolationError):
    code = "too_many_files"

    def __init__(self, limit: int) -> None:
        super().__init__(f"Too many files (max {limit})", limit=limit)


class StoredFileNotFoundError(NotFoundError):
    code = "file_not_found"

    def __init__(self, relative_path: str | None = None) -> None:
        super().__init__(
            f"File {relative_path} not found" if relative_path else "File not found",
            relative_path=relative_path,
        )


class InvalidStoragePathError(DomainError):
    code = "invalid_storage_path"
    default_message = "Invalid storage path"
