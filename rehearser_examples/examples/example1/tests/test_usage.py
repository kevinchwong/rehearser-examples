import unittest
from typing import Any
from unittest.mock import call, patch

from rehearser_examples.examples.example1.usage import Usage

from rehearser.mock_generator import MockGenerator


class UsageTestCase(unittest.TestCase):
    """
    Test Case for the Usage class.
    """

    def test_run_example_with_patch(self) -> None:
        """
        Test the run_example method of the Usage class with UserService and ProductService patched.
        """
        # Create mock objects
        mock_users = MockGenerator(
            interactions_src="./raw_files/rehearser_proxy/UserService/latest_interactions.json"
        ).create_mock()
        mock_products = MockGenerator(
            interactions_src="./raw_files/rehearser_proxy/ProductService/latest_interactions.json"
        ).create_mock()

        # Patch UserService and ProductService in Usage
        with patch(
            "rehearser_examples.examples.example1.usage.UserService",
            return_value=mock_users,
        ), patch(
            "rehearser_examples.examples.example1.usage.ProductService",
            return_value=mock_products,
        ):
            # Create Usage instance with mock services
            u = Usage(
                user_service=mock_users, product_service=mock_products
            )
            print()
            print(f"Rerun Usage.run_exmaple() with dependency injection")
            print(f"u.user_service: {type(u.user_service)}")
            print(f"u.product_service: {type(u.product_service)}")
            print()
            result = u.run_example()

            # Check method calls for mock_users
            expected_calls = [
                call.add_user(1, "User 1"),
                call.add_user(2, "User 2"),
                call.add_user(3, "User 3"),
                call.get_user(1),
                call.get_user(2),
                call.get_user(3),
            ]
            self.assertEqual(
                u.user_service.method_calls,
                expected_calls,
                "Patching for user_service Mock failed",
            )

            # Check method calls for mock_products
            expected_calls = [
                call.add_product(100, "Product 100"),
                call.add_product(200, "Product 200"),
                call.add_product(300, "Product 300"),
                call.get_product(100),
                call.get_product(200),
                call.get_product(300),
            ]
            self.assertEqual(
                u.product_service.method_calls,
                expected_calls,
                "Patching for product_service Mock failed",
            )

            self.assertTrue(result, "run_example() failed")



if __name__ == "__main__":
    unittest.main()
