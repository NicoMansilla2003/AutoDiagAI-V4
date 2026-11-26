"""Helpers for clearly separating user supplied text from agent instructions."""

from xml.sax.saxutils import escape


def untrusted_vehicle_input(value: str) -> str:
    """Escape markup and frame user text as data, never as agent instructions."""
    return "<untrusted_vehicle_report>\n" + escape(value, {"\"": "&quot;", "'": "&apos;"}) + "\n</untrusted_vehicle_report>"
