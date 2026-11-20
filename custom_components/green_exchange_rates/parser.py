
"""Parse rates from Telegram's public web preview."""
from __future__ import annotations

from html.parser import HTMLParser
import re
from html import unescape


class _MessageTextParser(HTMLParser):
    """Collect visible Telegram message text blocks."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.messages: list[str] = []
        self._capture_depth = 0
        self._parts: list[str] = []
        self._in_message = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "div" and "tgme_widget_message_text" in classes:
            self._in_message = True
            self._capture_depth = 1
            self._parts = []
        elif self._in_message:
            if tag not in ("br", "img", "hr"):
                self._capture_depth += 1
            if tag == "br":
                self._parts.append(" ")

    def handle_endtag(self, tag):
        if self._in_message:
            if tag not in ("br", "img", "hr"):
                self._capture_depth -= 1
            if self._capture_depth <= 0:
                text = " ".join("".join(self._parts).split())
                if text:
                    self.messages.append(text)
                self._in_message = False
                self._capture_depth = 0
                self._parts = []

    def handle_data(self, data):
        if self._in_message:
            self._parts.append(data)


_NUMBER = r"\d{1,3}(?:[.,]\d{1,2})?"
_RANGE = re.compile(rf"(?P<first>{_NUMBER})\s*[-–—]\s*(?P<second>{_NUMBER})")


def _parse_range(text: str, marker: str) -> tuple[float, float]:
    """Find the first numeric range following a currency marker."""
    pos = text.find(marker)
    if pos < 0:
        raise ValueError(f"Currency marker {marker!r} not found")
    match = _RANGE.search(text, pos + len(marker))
    if not match:
        raise ValueError(f"No numeric range found for {marker}")
    return (
        float(match.group("first").replace(",", ".")),
        float(match.group("second").replace(",", ".")),
    )


def parse_latest_rates(html: str) -> dict[str, float]:
    """Parse USD/EUR ranges from the last visible Telegram post."""
    parser = _MessageTextParser()
    parser.feed(unescape(html))
    if not parser.messages:
        raise ValueError("No Telegram message text found in page")

    latest_text = parser.messages[-1]
    usd_buy, usd_sell = _parse_range(latest_text, "🇺🇸")
    eur_buy, eur_sell = _parse_range(latest_text, "🇪🇺")

    return {
        "usd_buy": usd_buy,
        "usd_sell": usd_sell,
        "eur_buy": eur_buy,
        "eur_sell": eur_sell,
        "source_text": latest_text,
    }
