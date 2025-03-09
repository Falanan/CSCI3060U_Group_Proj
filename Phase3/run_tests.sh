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

###################
# DECIDE WHICH TESTS TO RUN
###################
if [[ "$TEST_ID" == "02" ]]; then
  # run only transfer tests
  run_transfer_tests

elif [[ "$TEST_ID" == "03" ]]; then
  # run only paybill tests
  run_paybill_tests

else
  # run all tests
  run_transfer_tests
  run_paybill_tests
fi
