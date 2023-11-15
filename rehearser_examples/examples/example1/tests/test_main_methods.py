from unittest.mock import Mock, patch

from rehearser.mock_generator import MockGenerator
from rehearser.rehearser_method import RehearserMethod


def main_method(i):
    print(f"Main! -> {i}")
    return i


# Rehersal
rm = RehearserMethod(main_method)
with patch("__main__.main_method", rm.get_proxy_method()):
    main_method(1)
    main_method(2)
    main_method(3)

rm.set_interactions_file_directory(
    "./rehearser_examples/examples/example2/tests/raw_files/"
)
rm.write_interactions_to_file()

# Unit test
mg = MockGenerator(
    interactions_src="./rehearser_examples/examples/example1/tests/raw_files/main_method/latest_interactions.json"
)
m1 = mg.create_mock()
with patch("__main__.main_method", m1):
    assert (main_method(), 1)
    assert (main_method(), 2)
    assert (main_method(), 3)
