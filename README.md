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

### **1. Install Rehearser**:
```bash
pip install rehearser
```
---
### **2. Creating a Rehearser Proxy**: 
- Component to be tested : `Usage`
- External services: `ProductService` and `UserService`

```mermaid
graph LR

Usgae["Usage"] -- uses --> ProductService["ProductService"]-- uses -->C["Cache"]
Usgae["Usage"] -- uses --> UserService["UserService"]-- uses -->C["Cache"]
```

- In this step, we create Rehearser Proxies for instances `ProductService()` and `UserService()`, respectively.
```python
rp_product = RehearserProxy(ProductService())
rp_user = RehearserProxy(UserService())
```
---
### **3. Generate Interactions**: 
Generate mock objects using the interactions created in the previous step.
```python
# Apply patches to UserService and ProductService
with patch(
    "rehearser_examples.examples.example1.usage.UserService",
    return_value=rp_user,
), patch(
    "rehearser_examples.examples.example1.usage.ProductService",
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
### **4. Write Unit Test**:
These will be your unit test body:
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