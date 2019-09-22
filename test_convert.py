import unittest
from convert import parse_body


class TestConvert(unittest.TestCase):

    def test_with_share(self):
        with open("test/body_with_share.txt", "r") as f:
            content = f.read()

            (foreign, message, datetime) = parse_body(content)
            self.assertEqual(foreign, "$53.24")
            self.assertEqual(message, "Patreon* Membership INTERNET GBR")
            self.assertEqual(datetime.isoformat(), "2019-09-01T13:22:00")

    def test_no_share(self):
        with open("test/body_no_share.txt", "r") as f:
            content = f.read()

            (foreign, message, datetime) = parse_body(content)
            self.assertEqual(foreign, "")
            self.assertEqual(message, "Sviezios bandeles Vilnius LTU")
            self.assertEqual(datetime.isoformat(), "2019-05-29T05:25:00")

    def test_no_utc_no_share(self):
        with open("test/body_no_utc_no_share.txt", "r") as f:
            content = f.read()

            (foreign, message, datetime) = parse_body(content)
            self.assertEqual(foreign, "")
            self.assertEqual(message, "CityBee Vilnius GBR")
            self.assertEqual(datetime.isoformat(), "2019-06-24T21:36:00")

    def test_transaction_update_no_share(self):
        with open("test/body_transaction_update_no_share.txt", "r") as f:
            content = f.read()

            (foreign, message, datetime) = parse_body(content)
            self.assertEqual(foreign, "")
            self.assertEqual(message, "AMZNMktplace amazon.co.uk GBR")
            self.assertEqual(datetime.isoformat(), "2019-08-07T07:19:00")

    def test_no_share_newline(self):
        with open("test/body_no_share_newline.txt", "r") as f:
            content = f.read()

            (foreign, message, datetime) = parse_body(content)
            self.assertEqual(foreign, "")
            self.assertEqual(message, "FAIRTIQ Fribourg CHE")
            self.assertEqual(datetime.isoformat(), "2019-06-13T03:37:00")


if __name__ == '__main__':
    unittest.main()
