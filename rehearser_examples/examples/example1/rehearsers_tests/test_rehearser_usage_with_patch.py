import unittest
from typing import Any
from unittest.mock import patch

from rehearser.rehearser_proxy import RehearserProxy
from rehearser_examples.examples.example1.services.product_service import ProductService
from rehearser_examples.examples.example1.services.user_service import UserService
from rehearser_examples.examples.example1.usage import Usage


class TestRehearserUsageWithPatch(unittest.TestCase):
    """
    Test Case for the Usage class with rehearser proxy.
    """

    def test_rehearser_run_example(self) -> None:
        """
        Test the run_example method of the Usage class with UserService and ProductService patched with rehearser proxy.
        """

        rp_product = RehearserProxy(ProductService())
        rp_user = RehearserProxy(UserService())

        with patch(
            "rehearser_examples.examples.example1.usage.UserService",
            return_value=rp_user,
        ), patch(
            "rehearser_examples.examples.example1.usage.ProductService",
            return_value=rp_product,
        ):
            u = Usage()
            u.run_example()

            # Generate interaction files
            u.user_service.write_interactions_to_file()
            u.product_service.write_interactions_to_file()


if __name__ == "__main__":
    unittest.main()
