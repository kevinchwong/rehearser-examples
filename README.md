# Quick Start
You can use `Rehearser` to build reliable unit tests quickly

----

### Development Flow:
```mermaid
graph LR

R["Rehearsal<br>runs"]--"interactions<br>file<br>case 1"-->A1["Adjust your<br>expectation"]-->C1["Create<br>Mocks"]-->U1("Unit Test 1")-->F["Finalize<br>Implementation"]
R["Rehearsal<br>runs"]--"interactions<br>file<br>case 2"-->A2["Adjust your<br>expectation"]-->C2["Create<br>Mocks"]-->U2("Unit Test 2")-->F["Finalize<br>Implementation"]
R["Rehearsal<br>runs"]--"interactions<br>file<br>case ..."-->A3["Adjust your<br>expectation"]-->C3["Create<br>Mocks"]-->U3("Unit Test ...")-->F["Finalize<br>Implementation"]
R["Rehearsal<br>runs"]--"interactions<br>file<br>case N"-->AN["Adjust your<br>expectation"]-->CN["Create<br>Mocks"]-->UN("Unit Test N")-->F["Finalize<br>Implementation"]
```

---

### **Install Rehearser**:
```bash
pip install rehearser
```
---
### **Example 1: Mock a method:**
```
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

rm.set_interactions_file_directory("./rehearser_examples/examples/example2/tests/raw_files/")
rm.write_interactions_to_file()

# Unit test
mg = MockGenerator(rm.get_interactions())
m1 = mg.create_mock()
with patch("__main__.main_method", m1):
    assert(main_method(), 1)
    assert(main_method(), 2)
    assert(main_method(), 3)
```

---

### **Example 2: Mock an instance**:

#### **1. Creating a Rehearser Proxy**: 
- Component to be tested : `Usage`
- External services: `ProductService` , `UserService` and `Cache`

```mermaid
graph LR

Usage["Usage<br>(Code to be tested here)"] -- uses --> ProductService["ProductService<br>(Add RehearserProxy here)"]-- uses -->C["Cache"]
Usage -- uses --> UserService["UserService<br>(Add RehearserProxy here)"]-- uses -->C["Cache"]
```

- In this step, we create Rehearser Proxies for instances `ProductService()` and `UserService()`, respectively.
```python
rp_product = RehearserProxy(ProductService())
rp_user = RehearserProxy(UserService())
```
---
#### **2. Generate Interactions**: 
Generate mock objects using the interactions created in the previous step:
```python
# Apply patches to UserService and ProductService
with patch(
    "rehearser_examples.examples.example2.usage.UserService",
    return_value=rp_user,
), patch(
    "rehearser_examples.examples.example2.usage.ProductService",
    return_value=rp_product,
):
    # Rehearsal run
    Usage().run_example()

    # Generate interactions files
    rp_user.set_interactions_file_directory("./raw_files/rehearser_proxy/")
    rp_user.write_interactions_to_file()

    rp_product.set_interactions_file_directory("./raw_files/rehearser_proxy/")
    rp_product.write_interactions_to_file()

```
- Notes: The interaction files are in json format, and you can adjust these thru editor manually before using these for further Mock object generation.
---
#### **3. Write Unit Test**:
```mermaid
graph LR

Usage["Usage<br>(Code to be tested here)"] -- uses --> ProductService["ProductService<br>(Mocked)"]
Usage -- uses --> UserService["UserService<br>(Mocked)"]
```
Unit test body:
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
    "rehearser_examples.examples.example2.usage.UserService",
    return_value=mock_users,
), patch(
    "rehearser_examples.examples.example2.usage.ProductService",
    return_value=mock_products,
):
    # Instantiate Usage with the mocked services
    result = Usage().run_example()

    # Insert your test assertions here
    self.assertTrue(result, "run_example() failed")
```