import unittest
from unittest.mock import patch
from typing import Any

from rehearser_examples.examples.example1.cache import Cache
from rehearser_examples.examples.example1.services.product_service import ProductService
from rehearser_examples.examples.example1.services.user_service import UserService
from rehearser_examples.examples.example1.usage import Usage
from rehearser.rehearser_proxy import RehearserProxy

class TestRehearserUsageWithPatch(unittest.TestCase):
    """
    Test Case for the Usage class with rehearser proxy.
    """

    @patch(
        "rehearser_examples.examples.example1.usage.UserService",
        return_value=RehearserProxy(UserService(Cache())),
    )
    @patch(
        "rehearser_examples.examples.example1.usage.ProductService",
        return_value=RehearserProxy(ProductService(Cache())),
    )
    def test_rehearser_run_example(
        self, rp_product: Any, rp_user: Any
    ) -> None:
        """
        Test the run_example method of the Usage class with UserService and ProductService patched with rehearser proxy.
        """
        u = Usage()
        u.run_example()
        
        # Generate interaction files
        u.user_service.write_interactions_to_file()
        u.product_service.write_interactions_to_file()


if __name__ == "__main__":
    unittest.main()