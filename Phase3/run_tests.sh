#!/usr/bin/env bash
#
# run_tests.sh
#
# Usage examples:
#   ./run_tests.sh           # runs ALL tests (both TRANSFER and PAYBILL)
#   ./run_tests.sh 02        # runs ONLY TRANSFER tests
#   ./run_tests.sh 03        # runs ONLY PAYBILL tests
#
# Make sure main.py and current_accounts_file.txt are in the same directory
# as this script, or update the paths below if needed.

# Path to your Python script:
PYTHON_SCRIPT="./main.py"

# Path to the current accounts file:
ACCOUNTS_FILE="./current_accounts_file.txt"

# The user can pass "02" for transfer or "03" for paybill, or nothing for all.
TEST_ID="$1"


run_login_tests() {
  echo "Running all LOGIN tests..."

  # We assume test cases are named login_01.inp ... login_05.inp (adjust the count as needed)
  for i in $(seq 1 7); do
    CASE_ID=$(printf "%02d" $i)
    INPUT_FILE="inputs/00_login_inputs/login${CASE_ID}_input.inp"
    OUT_FILE="outputs/00_login_outputs/00_login${CASE_ID}_output.out"
    ETF_FILE="transaction_outputs/00_login_transaction_outputs/login.etf"
    echo "  Running LOGIN test #$CASE_ID..."
    python3 "$PYTHON_SCRIPT" "$ACCOUNTS_FILE" "$INPUT_FILE" "$OUT_FILE" "$ETF_FILE"
  done

  echo "All LOGIN tests completed."
}



# A small helper function to run transfer tests
run_transfer_tests() {
  echo "Running all TRANSFER tests..."

  # We assume 12 test cases named transfer_01.inp ... transfer_12.inp
  for i in $(seq 1 12); do
    # zero-pad the test index (01, 02, ..., 12)
    CASE_ID=$(printf "%02d" $i)

    # Input file
    INPUT_FILE="inputs/02_transfer_inputs/transfer_${CASE_ID}.inp"

    # .out file
    OUT_FILE="outputs/02_transfer_outputs/02_test_${CASE_ID}.out"

    # .etf file
    ETF_FILE="transaction_outputs/02_transfer_transaction_outputs/02_test_${CASE_ID}.etf"

    echo "  Running TRANSFER test #$CASE_ID..."
    python3 "$PYTHON_SCRIPT" "$ACCOUNTS_FILE" "$INPUT_FILE" "$OUT_FILE" "$ETF_FILE"
  done

  echo "All TRANSFER tests completed."
}

# A small helper function to run paybill tests
run_paybill_tests() {
  echo "Running all PAYBILL tests..."

  # We assume 9 test cases named paybill_01.inp ... paybill_09.inp
  for i in $(seq 1 9); do
    CASE_ID=$(printf "%02d" $i)

    # Input file
    INPUT_FILE="inputs/03_paybill_inputs/paybill_${CASE_ID}.inp"

    # .out file
    OUT_FILE="outputs/03_paybill_outputs/03_test_${CASE_ID}.out"

    # .etf file
    ETF_FILE="transaction_outputs/03_paybill_transaction_outputs/03_test_${CASE_ID}.etf"

    echo "  Running PAYBILL test #$CASE_ID..."
    python3 "$PYTHON_SCRIPT" "$ACCOUNTS_FILE" "$INPUT_FILE" "$OUT_FILE" "$ETF_FILE"
  done

  echo "All PAYBILL tests completed."
}

##################################
# Helper: Run CHANGEPLAN tests (07)
##################################
run_changeplan_tests() {
  echo "Running all CHANGEPLAN tests..."
  # Assuming there are 8 test cases in inputs/07_changeplan_inputs
  for i in $(seq 1 8); do
    CASE_ID=$(printf "%02d" $i)
    INPUT_FILE="inputs/07_changeplan_inputs/changeplan${CASE_ID}.inp"
    # Actual output files are named with a prefix (07_test_) to distinguish from expected ones.
    OUT_FILE="outputs/07_changeplan_outputs/07_test_${CASE_ID}.out"
    ETF_FILE="transaction_outputs/07_changeplan_transaction_outputs/07_test_${CASE_ID}.etf"
    echo "  Running CHANGEPLAN test #$CASE_ID..."
    python3 "$PYTHON_SCRIPT" "$ACCOUNTS_FILE" "$INPUT_FILE" "$OUT_FILE" "$ETF_FILE"
  done
  echo "All CHANGEPLAN tests completed."
}

##################################
# Helper: Run DISABLE tests (08)
##################################
run_disable_tests() {
  echo "Running all DISABLE tests..."
  # Assuming there are 7 test cases in inputs/08_disable_inputs
  for i in $(seq 1 7); do
    CASE_ID=$(printf "%02d" $i)
    INPUT_FILE="inputs/08_disable_inputs/disable${CASE_ID}.inp"
    OUT_FILE="outputs/08_disable_outputs/08_test_${CASE_ID}.out"
    ETF_FILE="transaction_outputs/08_disable_transaction_outputs/08_test_${CASE_ID}.etf"
    echo "  Running DISABLE test #$CASE_ID..."
    python3 "$PYTHON_SCRIPT" "$ACCOUNTS_FILE" "$INPUT_FILE" "$OUT_FILE" "$ETF_FILE"
  done
  echo "All DISABLE tests completed."
}

##################################
# Helper: Run LOGOUT tests
##################################
run_logout_tests() {
  echo "Running all LOGOUT tests..."
  # Assuming there are 10 test cases in inputs/logout_inputs
  for i in $(seq 1 10); do
    CASE_ID=$(printf "%02d" $i)
    INPUT_FILE="inputs/logout_inputs/logout${CASE_ID}.inp"
    OUT_FILE="outputs/logout_outputs/logout_test_${CASE_ID}.out"
    ETF_FILE="transaction_outputs/logout_transaction_outputs/logout_test_${CASE_ID}.etf"
    echo "  Running LOGOUT test #$CASE_ID..."
    python3 "$PYTHON_SCRIPT" "$ACCOUNTS_FILE" "$INPUT_FILE" "$OUT_FILE" "$ETF_FILE"
  done
  echo "All LOGOUT tests completed."
}

###################
# DECIDE WHICH TESTS TO RUN
###################



if [[ "$TEST_ID" == "00" ]]; then
  # run only transfer tests
  run_login_tests
elif [[ "$TEST_ID" == "02" ]]; then
  # run only transfer tests
  run_transfer_tests
elif [[ "$TEST_ID" == "03" ]]; then
  # run only paybill tests
  run_paybill_tests
elif [[ "$TEST_ID" == "07" ]]; then
  run_changeplan_tests
elif [[ "$TEST_ID" == "08" ]]; then
  run_disable_tests
elif [[ "$TEST_ID" == "logout" ]]; then
  run_logout_tests
else
  # run all tests
  run_transfer_tests
  run_paybill_tests
  run_changeplan_tests
  run_disable_tests
  run_logout_tests
fi
