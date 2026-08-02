"""Pydantic models describing API responses."""

from pydantic import BaseModel


class ProcessedFile(BaseModel):
    """Name of a generated output file inside the processed directory."""

    output_file: str


class ServiceInfo(BaseModel):
    """Basic metadata about the running service."""

    name: str
    version: str
    endpoints: list[str]
