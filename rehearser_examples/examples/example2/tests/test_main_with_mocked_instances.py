from unittest.mock import Mock, patch

from rehearser.mock_generator import MockGenerator
from rehearser.rehearser_proxy import RehearserProxy


class ExternalService:
    def __init__(self):
        pass

    def long_run_method(self, x):
        print(f"Take a long time to run in {x*x} days...")
        return x * x


# Run a Rehearsal
rehearser = RehearserProxy(ExternalService())
with patch("__main__.ExternalService", return_value=rehearser):
    service = ExternalService()
    print(f"type of patched service: {type(service)}")
    a = service.long_run_method(1)
    b = service.long_run_method(2)
    c = service.long_run_method(3)

    # Your logic
    res = a + b + c
    print(res)


# Prepare interactions files
rehearser.set_interactions_file_directory(
    "./rehearser_examples/examples/example2/tests/raw_files/"
)
rehearser.write_interactions_to_file()


# Unit test
mock = MockGenerator(
    interactions_src="./rehearser_examples/examples/example2/tests/raw_files/ExternalService/latest_interactions.json"
).create_mock()
with patch("__main__.ExternalService", return_value=mock):
    # Replay the long time running method output with the mocked method
    service = ExternalService()
    print(f"type of mocked service: {type(service)}")
    a = service.long_run_method(1)
    b = service.long_run_method(2)
    c = service.long_run_method(3)

    # Your logic to be tested:
    result = a + b + c

    print(
        f"Result from mockers: {result} where mocked a={a}, mocked b={b}, and mocked c={c}"
    )
    # Verify the result
    assert res == 14
