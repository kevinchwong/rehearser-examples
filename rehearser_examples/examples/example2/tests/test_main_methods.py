from unittest.mock import Mock, patch

from rehearser.mock_generator import MockGenerator
from rehearser.rehearser_method import RehearserMethod


def main_method(i):
    print(f"{i}: I am Main!")
    return i


rm = RehearserMethod(main_method)

# rehersal
with patch("__main__.main_method", rm.get_proxy_method()):
    main_method(1)
    main_method(2)
    main_method(3)

print(f"rm._method: {rm._method}")
print(f"rm.get_interactions(): {rm.get_interactions()}")

rm.set_interactions_file_directory("./tests/raw_files/")
rm.write_interactions_to_file()

# make sure 2 mocks from one mg have it own interactions queue
mg = MockGenerator(rm.get_interactions())
m1 = mg.create_mock()
m2 = mg.create_mock()
with patch("__main__.main_method", m1):
    print(main_method())
    print(main_method())
    print(main_method())
with patch("__main__.main_method", m2):
    print(main_method())
    print(main_method())
    print(main_method())
