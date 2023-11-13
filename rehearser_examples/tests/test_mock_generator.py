import json
import unittest
from rehearser.mock_generator import MockGenerator
from rehearser.rehearser_proxy import RehearserProxy

class TestRealMockGenerator(unittest.TestCase):

    def test_real_mock_generator(self):

        class Calculator:
            def add(self, a, b):
                return a + b

            def divide(self, a, b):
                if b == 0:
                    raise ValueError("Cannot divide by zero")
                return a / b

        calculator = Calculator()

        proxy = RehearserProxy(calculator)
        
        # Record interactions
        proxy.status = "inactive"
        print(proxy.status)
        print(proxy.add(2, 3))
        print(proxy.divide(10, 2))
        proxy.status = "active"
        print(proxy.status)
        try:
            print(proxy.divide(10, 0))
        except Exception as e:
            print(e)

        # Create Mock Calculator object
        interactions = proxy.get_interactions()
        mock = MockGenerator(interactions).create_mock()

        # Verify
        mock.status = "inactive"
        self.assertEqual(mock.status, "inactive")
        self.assertEqual(mock.add(2, 3), 5)
        self.assertEqual(mock.divide(10, 2), 5.0)
        mock.status = "active"
        self.assertEqual(mock.status, "active")
        with self.assertRaises(ValueError):
            mock.divide(10, 0)    
        self.assertEqual(mock.divide(10, 0), None)
                
        # Check reherasal proxy interactions
        interactions_python_dict = proxy.get_interactions()
        interactions_serialable_json = proxy.get_interactions_serializable_json() 
        interactions_serialable_json_str = json.dumps(interactions_serialable_json, indent=2)
        print(f"interactions_serialable_json_str: {interactions_serialable_json_str}")
        
        # Create mock object from rehearser proxy interactions
        # interactions_src can be in any type of the following:
        # 1. python dict with non-serializable objects
        # 2. json object just contains serializable value
        # 3. json string
        mocks_array = []
        mocks_array += [MockGenerator(interactions_src=interactions_python_dict).create_mock()]
        mocks_array += [MockGenerator(interactions_src=interactions_serialable_json).create_mock()]
        mocks_array += [MockGenerator(interactions_src=interactions_serialable_json_str).create_mock()]
        
        for mock in mocks_array:
            mock.status = "inactive"
        check_result_array = [mock.status for mock in mocks_array]
        print(check_result_array)
        self.assertEqual(check_result_array[1:], check_result_array[:-1], "All elements are not the same")

        for mock in mocks_array:
            mock.status = "active"
        check_result_array = [mock.status for mock in mocks_array]
        print(check_result_array)
        self.assertEqual(check_result_array[1:], check_result_array[:-1], "All elements are not the same")

        try:
            check_result_array = [mock.divide() for mock in mocks_array]
            print(check_result_array)
            self.assertEqual(check_result_array[1:], check_result_array[:-1], "All elements are not the same")
        except Exception as e:
            print(type(e),e)

        try:
            check_result_array = [mock.add() for mock in mocks_array]
            print(check_result_array)
            self.assertEqual(check_result_array[1:], check_result_array[:-1], "All elements are not the same")
        except Exception as e:
            print(type(e),e)

        for mock in mocks_array:
            with self.assertRaises(ValueError):
                try:
                    mock.divide()
                except Exception as e:
                    print(type(e),e)
                    raise e

        
if __name__ == "__main__":
    unittest.main()