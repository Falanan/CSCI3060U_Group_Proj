### **README.md**

# CSCI 3060U Course Project - Winter 2025

## **Phase #1 - Front End Requirements**   

## **Project Overview**
This repository contains a comprehensive **test suite** for the **Front End of the Banking System** as required in **Phase #1** of the CSCI 3060U Course Project. The purpose of this phase is to analyze the Front End requirements and develop a **complete set of requirements tests** without writing any code.  

Each test case includes:
- **Test inputs (`.inp` files)**: Simulated session input streams.
- **Expected outputs (`.out` files)**: The correct system response.
- **Transaction logs (`.etf` files)**: The expected transaction records.

All test cases are systematically **organized in directories** for clarity.

---

## **Submission Contents**
This repository includes the following required components:

1. **📄 List of Test Cases (`test_cases.docx`)**  
   - A **table listing all test cases** with their intended purpose.  
   - Ensures all required behaviors and constraints are tested.  

2. **📂 Test Files**  
   - **Test input files (`.inp`)** for each scenario.  
   - **Expected output files (`.out`, `.etf`)** for verification.  
   - Files are organized by transaction type.  

3. **📄 Test Plan (`test_plan.docx`)**  
   - **Explains how tests are structured** in directories.  
   - **Describes how tests will be executed** using shell scripts.  
   - **Details how results are stored and compared** with future runs.  

---

## **Folder Structure**
The test files are **organized by transaction type**, making it easy to manage and execute tests.

```
current_accounts_file.txt  (Shared test account data)
inputs                     (Contains all test input files)
│  ├── 00_login_inputs/
│  ├── 01_withdrawal_inputs/
│  ├── 02_transfer_inputs/
│  ├── 03_paybill_inputs/
│  ├── 04_deposit_inputs/
│  ├── 05_create_inputs/
│  ├── 06_delete_inputs/
│  ├── 07_changeplan_inputs/
│  ├── 08_disable_inputs/
│  ├── 09_logout_inputs/
outputs                    (Contains expected system responses)
│  ├── 00_login_outputs/
│  ├── 01_withdrawal_outputs/
│  ├── 02_transfer_outputs/
│  ├── 03_paybill_outputs/
│  ├── 04_deposit_outputs/
│  ├── 05_create_outputs/
│  ├── 06_delete_outputs/
│  ├── 07_changeplan_outputs/
│  ├── 08_disable_outputs/
│  ├── 09_logout_outputs/
transaction_outputs         (Contains expected transaction logs)
│  ├── 01_withdrawal_transaction_outputs/
│  ├── 02_transfer_transaction_outputs/
│  ├── 03_paybill_transaction_outputs/
│  ├── 04_deposit_transaction_outputs/
│  ├── 05_create_transaction_outputs/
│  ├── 06_delete_transaction_outputs/
│  ├── 07_changeplan_transaction_outputs/
│  ├── 08_disable_transaction_outputs/
│  ├── 09_logout_transaction_outputs/
```
📌 *This structure was generated using the `tree` command (installed via Homebrew `brew install tree`).*  
To generate this structure manually, use:
```bash
tree -a
```

## **License**
This project is part of **CSCI 3060U** and is intended for academic use only.