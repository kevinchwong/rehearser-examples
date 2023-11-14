import json
import unittest
from rehearser.mock_generator import MockGenerator
from rehearser.rehearser_proxy import RehearserProxy

class TestRehearserProxyAndMock(unittest.TestCase):

    def test_rehearser_proxy_and_mock(self):

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
        proxy.count = 0
        print(proxy.count)
        proxy.count = 1
        print(proxy.count)
        proxy.count = 2
        print(proxy.count)
        proxy.count += 3
        print(proxy.count)

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
        
        # Assertions 1
        self.assertEqual(mock.status, "inactive")
        self.assertEqual(mock.status, "active")
        self.assertEqual(mock.add(2, 3), 5)
        self.assertEqual(mock.divide(10, 2), 5.0)
        with self.assertRaises(ValueError):
            mock.divide(10, 0)    
        with self.assertRaises(StopIteration):
            mock.divide(10, 0)
        self.assertEqual(mock.count, 0)
        self.assertEqual(mock.count, 1)
        self.assertEqual(mock.count, 2)
        self.assertEqual(mock.count, 2)
        self.assertEqual(mock.count, 5)
        with self.assertRaises(StopIteration):
            mock.count         

        
        # Create 3 Mock objects from the different format of same interactions
        interactions_python_dict = proxy.get_interactions()
        interactions_serialable_json = proxy.get_interactions_serializable_json() 
        interactions_serialable_json_str = json.dumps(interactions_serialable_json, indent=2)
        mocks_array = []
        mocks_array += [MockGenerator(interactions_src=interactions_python_dict).create_mock()]
        mocks_array += [MockGenerator(interactions_src=interactions_serialable_json).create_mock()]
        mocks_array += [MockGenerator(interactions_src=interactions_serialable_json_str).create_mock()]
        
        # Assertions 2
        check_result_array = [mock.status for mock in mocks_array]
        print(check_result_array)
        self.assertEqual(check_result_array[1:], check_result_array[:-1], "All elements are not the same")
        self.assertEqual(check_result_array[0], "inactive", "mock.status does not matched")

        check_result_array = [mock.status for mock in mocks_array]
        print(check_result_array)
        self.assertEqual(check_result_array[1:], check_result_array[:-1], "All elements are not the same")
        self.assertEqual(check_result_array[0], "active", "mock.status does not matched")

        for mock in mocks_array:
            with self.assertRaises(StopIteration):
                try:
                    mock.status
                except Exception as e:
                    print(type(e),e)
                    raise e

        check_result_array = [mock.divide() for mock in mocks_array]
        print(check_result_array)
        self.assertEqual(check_result_array[1:], check_result_array[:-1], "All elements are not the same")

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

        for mock in mocks_array:
            with self.assertRaises(StopIteration):
                try:
                    mock.divide()
                except Exception as e:
                    print(type(e),e)
                    raise e
        
if __name__ == "__main__":
    unittest.main()