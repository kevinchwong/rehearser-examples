# Quick Start

This is the code we wanted to test:
```python
def run_example(self):
    """
        This is the code that we want to test.
    """

    # Create users
    self.user_service.add_user(1, "User 1")
    self.user_service.add_user(2, "User 2")
    self.user_service.add_user(3, "User 3")

    # Create products
    self.product_service.add_product(100, "Product 100")
    self.product_service.add_product(200, "Product 200")
    self.product_service.add_product(300, "Product 300")

    # List users
    print("Users:")
    for user_id in range(1, 4):
        user_data = self.user_service.get_user(user_id)
        print(f"User ID: {user_id}, User Data: {user_data}")

    # List products
    print("Products:")
    for product_id in range(100, 400, 100):
        product_data = self.product_service.get_product(product_id)
        print(f"Product ID: {product_id}, Product Data: {product_data}")
        
    return True
```

## **Installation**:

```bash
pip install rehearser
```

## **Creating a Rehearser Proxy**: 

```python
from rehearser import RehearserProxy
from examples.example1.usage import ProductService, UserService

product_service = ProductService()
user_service = UserService()

rp_product = RehearserProxy(product_service)
rp_user = RehearserProxy(user_service)
```

In this example, `rp_product` and `rp_user` serve as proxies for `product_service` and `user_service`, respectively.

## **Generate Interactions**: 
The following code shows how to generate mock objects using the interaction files created in the previous step.
```python
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

    # Rehearsal run
    result = Usage().run_example()

    # Generate interactions files
    rp_user.set_interactions_file_directory("./raw_files/rehearser_proxy/")
    rp_user.write_interactions_to_file()
    rp_product.set_interactions_file_directory("./raw_files/rehearser_proxy/")
    rp_product.write_interactions_to_file()

```

## **Test with Generated Mock using Interaction Files**:
Run your unit test patched with mocks now.
```python
# Instantiate mock objects
mock_users = MockGenerator(
    interactions_src="./raw_files/rehearser_proxy/UserService/latest_interactions.json"
).create_mock()
mock_products = MockGenerator(
    interactions_src="./raw_files/rehearser_proxy/ProductService/latest_interactions.json"
).create_mock()

# Apply patches to UserService and ProductService
with patch(
    "rehearser_examples.examples.example1.usage.UserService",
    return_value=mock_users,
), patch(
    "rehearser_examples.examples.example1.usage.ProductService",
    return_value=mock_products,
):
    # Instantiate Usage with the mocked services
    result = Usage().run_example()

    # Insert your test assertions here
    self.assertTrue(result, "run_example() failed")
```
