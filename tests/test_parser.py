import unittest
from custom_components.green_exchange.parser import parse_latest_rates


class ParserTests(unittest.TestCase):
    def test_parse_ranges_from_latest_message(self):
        html = """
        <div class="tgme_widget_message_text">Old 🇺🇸 45,00-45,20 🇪🇺 50,00-50,20</div>
        <div class="tgme_widget_message_text">🇺🇸 46,10-46,35 🇪🇺 51,80-52,20</div>
        """
        rates = parse_latest_rates(html)
        self.assertEqual(rates["usd_buy"], 46.10)
        self.assertEqual(rates["usd_sell"], 46.35)
        self.assertEqual(rates["eur_buy"], 51.80)
        self.assertEqual(rates["eur_sell"], 52.20)


if __name__ == "__main__":
    unittest.main()
