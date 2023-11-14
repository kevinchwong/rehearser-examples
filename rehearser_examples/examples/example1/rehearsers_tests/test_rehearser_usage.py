import json
import unittest
from typing import Any, Dict, List
from unittest.mock import Mock

from rehearser_examples.examples.example1.cache import Cache
from rehearser_examples.examples.example1.services.product_service import ProductService
from rehearser_examples.examples.example1.services.user_service import UserService
from rehearser_examples.examples.example1.usage import Usage
from rehearser.mock_generator import MockGenerator
from rehearser.rehearser_proxy import RehearserProxy


class TestRehearserUsage(unittest.TestCase):
    """
    rehearser Test for the Usage class with rehearser proxy.
    - Generate interactions file with rehearser proxy
    """

    def test_rehearser_run_example(self):
        """
        Test the run_example method of the Usage class with UserService and ProductService patched with rehearser proxy.
        """

        # Patch the real services with rehearser proxy services
        rp_user = RehearserProxy(UserService())
        rp_product = RehearserProxy(ProductService())

        # Call the run_example method
        Usage(
            user_service=rp_user,
            product_service=rp_product,
        ).run_example()

        # Check reherasal proxy interactions
        interactions_user_python_dict: Dict[
            str, Any
        ] = rp_user.get_interactions()
        interactions_user_serialable_json: Dict[
            str, Any
        ] = rp_user.get_interactions_serializable_json()
        interactions_user_serialable_json_str: str = json.dumps(
            interactions_user_serialable_json, indent=2
        )
        print(
            f"interactions_user_serialable_json_str: {interactions_user_serialable_json_str}"
        )

        # Write interactions to file
        rp_user.set_interactions_file_directory(
            "./raw_files/rehearser_proxy/"
        )
        rp_user.write_interactions_to_file()
        rp_product.set_interactions_file_directory(
            "./raw_files/rehearser_proxy/"
        )
        rp_product.write_interactions_to_file()

        # Line up all 3 mock objects generated to an array, Make sure their results are all the same
        mocks_array: List[Mock] = []
        # MockGenerator can generate mock object from 3 types of interactions:
        # 1. python dict with non-serializable objects
        # 2. json object just contains serializable value
        # 3. json string
        mocks_array += [
            MockGenerator(interactions_src=interactions_user_python_dict).create_mock()
        ]
        mocks_array += [
            MockGenerator(
                interactions_src=interactions_user_serialable_json
            ).create_mock()
        ]
        mocks_array += [
            MockGenerator(
                interactions_src=interactions_user_serialable_json_str
            ).create_mock()
        ]

        # Compare the results of the 3 generated mock objects
        for mock in mocks_array:
            mock.status = "inactive"
        check_result_array = [mock.status for mock in mocks_array]
        print(check_result_array)
        self.assertEqual(
            check_result_array[1:],
            check_result_array[:-1],
            "All elements are not the same",
        )

        for mock in mocks_array:
            mock.status = "active"
        check_result_array = [mock.status for mock in mocks_array]
        print(check_result_array)
        self.assertEqual(
            check_result_array[1:],
            check_result_array[:-1],
            "All elements are not the same",
        )

        for i in range(1, 4, 1):
            check_result_array = [mock.add_user() for mock in mocks_array]
            print(f"{i}:{check_result_array}")
            self.assertEqual(
                check_result_array[1:],
                check_result_array[:-1],
                "All elements are not the same",
            )
            self.assertEqual(check_result_array[0], None, "Result not correct")

        # For the name of the method called which are not recorded in the interactions file, a Mock object will be returned
        for i in range(4, 5, 1):
            check_result_array = [mock.wrong_method() for mock in mocks_array]
            print(f"{i}:{check_result_array}")
            for mock_obj in check_result_array:
                self.assertTrue(
                    isinstance(mock_obj, Mock), "It is supposed to be a Mock object"
                )

        for i in range(5, 8, 1):
            check_result_array = [mock.get_user() for mock in mocks_array]
            print(f"{i}:{check_result_array}")
            self.assertEqual(
                check_result_array[1:],
                check_result_array[:-1],
                "All elements are not the same",
            )
            self.assertEqual(
                check_result_array[0], str.encode(f"User {i-4}"), "Result not correct"
            )

        # For the behaviors that are not recorded in the interactions file, the mock object will raise StopIteration
        for i in range(8, 9, 1):
            for mock in mocks_array:
                with self.assertRaises(StopIteration):
                    mock.get_user()


if __name__ == "__main__":
    unittest.main()
