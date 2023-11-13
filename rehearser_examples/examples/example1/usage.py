from rehearser_examples.examples.example1.services.product_service import ProductService
from rehearser_examples.examples.example1.services.user_service import UserService

class Usage:
    
    def __init__(self, user_service=None, product_service=None):
        """
            Initialize Usage class.
        """
        self.user_service = user_service if user_service else UserService() 
        self.product_service = product_service if product_service else ProductService()
        
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

