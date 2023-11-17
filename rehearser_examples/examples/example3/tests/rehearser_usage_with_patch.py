from unittest.mock import patch

from rehearser.rehearser_proxy import RehearserProxy
from rehearser_examples.examples.example3.services.product_service import ProductService
from rehearser_examples.examples.example3.services.user_service import UserService
from rehearser_examples.examples.example3.usage import Usage


rp_product = RehearserProxy(ProductService())
rp_user = RehearserProxy(UserService())

with patch(
    "rehearser_examples.examples.example3.usage.UserService",
    return_value=rp_user,
), patch(
    "rehearser_examples.examples.example3.usage.ProductService",
    return_value=rp_product,
):
    u = Usage()
    u.run_example()

    # Generate interaction files
    u.user_service.interactions_file_directory="./rehearser_examples/examples/example3/tests/raw_files/rehearser_proxy/"
    u.user_service.write_interactions_to_file()
    u.product_service.interactions_file_directory="./rehearser_examples/examples/example3/tests/raw_files/rehearser_proxy/"
    u.product_service.write_interactions_to_file()
