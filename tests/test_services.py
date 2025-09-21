import unittest
from unittest.mock import patch


class TestServicesValidation(unittest.TestCase):
    def test_request_token_requires_user_id(self):
        from services import request_token
        with self.assertRaisesRegex(ValueError, "user_id"):
            request_token({})

    def test_token_status_requires_fields(self):
        from services import token_status
        with self.assertRaisesRegex(ValueError, "token"):
            token_status({"user_id": 1})
        with self.assertRaisesRegex(ValueError, "user_id"):
            token_status({"token": "t"})

    def test_request_otp_requires_user_id(self):
        from services import request_otp
        with self.assertRaisesRegex(ValueError, "user_id"):
            request_otp({})

    def test_validate_otp_requires_fields(self):
        from services import validate_otp
        with self.assertRaisesRegex(ValueError, "otp_code"):
            validate_otp({"user_id": 1})
        with self.assertRaisesRegex(ValueError, "user_id"):
            validate_otp({"otp_code": 123456})


class TestServicesCalls(unittest.TestCase):
    @patch("client.make_request")
    def test_request_token_calls_endpoint(self, mk):
        from services import request_token
        request_token({"user_id": 1}, verify=False)
        args, kwargs = mk.call_args
        self.assertEqual(kwargs.get("endpoint"), "tokens")
        self.assertEqual(kwargs.get("method"), "POST")
        self.assertIn("headers", kwargs)
        self.assertIn("data", kwargs)

    @patch("client.make_request")
    def test_token_status_calls_endpoint(self, mk):
        from services import token_status
        token_status({"token": "t", "user_id": 1})
        args, kwargs = mk.call_args
        self.assertEqual(kwargs.get("endpoint"), "tokens/status")

    @patch("client.make_request")
    def test_request_otp_calls_endpoint(self, mk):
        from services import request_otp
        request_otp({"user_id": 1})
        args, kwargs = mk.call_args
        self.assertEqual(kwargs.get("endpoint"), "otp")

    @patch("client.make_request")
    def test_validate_otp_calls_endpoint(self, mk):
        from services import validate_otp
        validate_otp({"otp_code": 123456, "user_id": 1})
        args, kwargs = mk.call_args
        self.assertEqual(kwargs.get("endpoint"), "otp/validate")


if __name__ == "__main__":
    unittest.main()

