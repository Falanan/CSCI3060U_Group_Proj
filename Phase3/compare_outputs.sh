#!/usr/bin/env bash
#
# compare_outputs.sh
#
# Usage:
#   ./compare_outputs.sh         # compares ALL tests
#   ./compare_outputs.sh 02      # compares ONLY TRANSFER tests
#   ./compare_outputs.sh 03      # compares ONLY PAYBILL tests
#
# This script compares actual outputs (.out/.etf) to expected outputs,
# printing which cases passed or failed. If there's a mismatch, we also
# show a short diff snippet to help you see what's different.

TEST_ID="$1"

##################################
# Helper: Compare one .out and one .etf
##################################
compare_one_test() {
  local label="$1"          # e.g. "TRANSFER test #01"
  local actual_out="$2"
  local expected_out="$3"
  local actual_etf="$4"
  local expected_etf="$5"

  # Default results
  local out_result="FAIL"
  local etf_result="FAIL"

  # Make sure the files exist; if not, the diff is meaningless.
  if [[ ! -f "$actual_out" ]]; then
    echo "$label: FAIL - Missing actual .out file: $actual_out"
    return
  fi
  if [[ ! -f "$expected_out" ]]; then
    echo "$label: FAIL - Missing expected .out file: $expected_out"
    return
  fi
  if [[ ! -f "$actual_etf" ]]; then
    echo "$label: FAIL - Missing actual .etf file: $actual_etf"
    return
  fi
  if [[ ! -f "$expected_etf" ]]; then
    echo "$label: FAIL - Missing expected .etf file: $expected_etf"
    return
  fi

  # Compare .out
  if diff -w -B --strip-trailing-cr "$actual_out" "$expected_out" >/dev/null 2>&1; then
    out_result="PASS"
  else
    # Show a snippet of the diff so you can see what's different
    echo "--------- DIFF for $label .out ---------"
    diff -w -B --strip-trailing-cr -u "$actual_out" "$expected_out" | head -20
    echo "----------------------------------------"
  fi

  # Compare .etf
  if diff -w -B --strip-trailing-cr "$actual_etf" "$expected_etf" >/dev/null 2>&1; then
    etf_result="PASS"
  else
    echo "--------- DIFF for $label .etf ---------"
    diff -w -B --strip-trailing-cr -u "$actual_etf" "$expected_etf" | head -20
    echo "----------------------------------------"
  fi

  # Summarize
  if [[ "$out_result" == "PASS" && "$etf_result" == "PASS" ]]; then
    echo "$label: PASS"
  else
    echo "$label: FAIL (out=$out_result, etf=$etf_result)"
  fi
}

##################################
# LOGIN comparison
##################################
compare_login_outputs() {
  echo "Comparing Login outputs..."
    for i in $(seq 1 7); do
    CASE_ID=$(printf "%02d" $i)

    # -- Actual files
    local actual_out="outputs/00_login_outputs/00_login${CASE_ID}_output.out"
    local actual_etf="transaction_outputs/00_login_transaction_outputs/login.etf"

    # -- Expected files
    local expected_out="outputs/00_login_outputs/login${CASE_ID}_output.out"
    local expected_etf="transaction_outputs/00_login_transaction_outputs/login.etf"

    # Now compare
    local label="Login test #$CASE_ID"
    compare_one_test "$label" "$actual_out" "$expected_out" "$actual_etf" "$expected_etf"
  done
}

##################################
# WITHDRAWAL comparison
##################################
compare_withdrawal_outputs() {
  echo "Comparing WITHDRAWAL outputs..."
    for i in $(seq 1 7); do
    CASE_ID=$(printf "%02d" $i)

    # -- Actual files
    local actual_out="outputs/01_withdrawal_outputs/withdrawal${CASE_ID}_test_output.out"
    local actual_etf="transaction_outputs/01_withdrawal_transaction_outputs/withdrawal_test_${CASE_ID}.etf"

    # -- Expected files
    local expected_out="outputs/01_withdrawal_outputs/withdrawal${CASE_ID}_output.out"
    local expected_etf="transaction_outputs/01_withdrawal_transaction_outputs/withdrawal_${CASE_ID}.etf"

    # Now compare
    local label="WITHDRAWAL test #$CASE_ID"
    compare_one_test "$label" "$actual_out" "$expected_out" "$actual_etf" "$expected_etf"
  done
}


##################################
# TRANSFER comparison
##################################
compare_transfer_outputs() {
  echo "Comparing TRANSFER outputs..."

  # We have 12 test cases
  for i in $(seq 1 12); do
    CASE_ID=$(printf "%02d" $i)

    # -- Actual files
    local actual_out="outputs/02_transfer_outputs/02_test_${CASE_ID}.out"
    local actual_etf="transaction_outputs/02_transfer_transaction_outputs/02_test_${CASE_ID}.etf"

    # -- Expected files
    local expected_out="outputs/02_transfer_outputs/transfer_${CASE_ID}.out"
    local expected_etf="transaction_outputs/02_transfer_transaction_outputs/transfer_${CASE_ID}.etf"

    # Now compare
    local label="TRANSFER test #$CASE_ID"
    compare_one_test "$label" "$actual_out" "$expected_out" "$actual_etf" "$expected_etf"
  done
}

##################################
# PAYBILL comparison
##################################
compare_paybill_outputs() {
  echo ""
  echo "Comparing PAYBILL outputs..."

  # We have 9 test cases
  for i in $(seq 1 9); do
    CASE_ID=$(printf "%02d" $i)

    # -- Actual
    local actual_out="outputs/03_paybill_outputs/03_test_${CASE_ID}.out"
    local actual_etf="transaction_outputs/03_paybill_transaction_outputs/03_test_${CASE_ID}.etf"

    # -- Expected
    local expected_out="outputs/03_paybill_outputs/paybill_${CASE_ID}.out"
    local expected_etf="transaction_outputs/03_paybill_transaction_outputs/paybill_${CASE_ID}.etf"

    local label="PAYBILL test #$CASE_ID"
    compare_one_test "$label" "$actual_out" "$expected_out" "$actual_etf" "$expected_etf"
  done
}

##################################
# CHANGEPLAN comparison (07)
##################################
compare_changeplan_outputs() {
  echo ""
  echo "Comparing CHANGEPLAN outputs..."
  # For CHANGEPLAN, actual output files have a "07_test_" prefix.
  for i in $(seq 1 8); do
    CASE_ID=$(printf "%02d" $i)
    local actual_out="outputs/07_changeplan_outputs/07_test_${CASE_ID}.out"
    local actual_etf="transaction_outputs/07_changeplan_transaction_outputs/07_test_${CASE_ID}.etf"
    local expected_out="outputs/07_changeplan_outputs/changeplan${CASE_ID}.out"
    local expected_etf="transaction_outputs/07_changeplan_transaction_outputs/changeplan${CASE_ID}.etf"
    local label="CHANGEPLAN test #$CASE_ID"
    compare_one_test "$label" "$actual_out" "$expected_out" "$actual_etf" "$expected_etf"
  done
}

##################################
# DISABLE comparison (08)
##################################
compare_disable_outputs() {
  echo ""
  echo "Comparing DISABLE outputs..."
  for i in $(seq 1 7); do
    CASE_ID=$(printf "%02d" $i)
    local actual_out="outputs/08_disable_outputs/08_test_${CASE_ID}.out"
    local actual_etf="transaction_outputs/08_disable_transaction_outputs/08_test_${CASE_ID}.etf"
    local expected_out="outputs/08_disable_outputs/disable${CASE_ID}.out"
    local expected_etf="transaction_outputs/08_disable_transaction_outputs/disable${CASE_ID}.etf"
    local label="DISABLE test #$CASE_ID"
    compare_one_test "$label" "$actual_out" "$expected_out" "$actual_etf" "$expected_etf"
  done
}

##################################
# LOGOUT comparison
##################################
compare_logout_outputs() {
  echo ""
  echo "Comparing LOGOUT outputs..."
  for i in $(seq 1 10); do
    CASE_ID=$(printf "%02d" $i)
    local actual_out="outputs/logout_outputs/logout_test_${CASE_ID}.out"
    local actual_etf="transaction_outputs/logout_transaction_outputs/logout_test_${CASE_ID}.etf"
    local expected_out="outputs/logout_outputs/logout${CASE_ID}.out"
    local expected_etf="transaction_outputs/logout_transaction_outputs/logout${CASE_ID}.etf"
    local label="LOGOUT test #$CASE_ID"
    compare_one_test "$label" "$actual_out" "$expected_out" "$actual_etf" "$expected_etf"
  done
}


##################################
# Decide which tests to compare
##################################

if [[ "$TEST_ID" == "00" ]]; then
  compare_login_outputs
elif [[ "$TEST_ID" == "01" ]]; then
  compare_withdrawal_outputs
elif [[ "$TEST_ID" == "02" ]]; then
  compare_transfer_outputs
elif [[ "$TEST_ID" == "03" ]]; then
  compare_paybill_outputs
elif [[ "$TEST_ID" == "07" ]]; then
  compare_changeplan_outputs
elif [[ "$TEST_ID" == "08" ]]; then
  compare_disable_outputs
elif [[ "$TEST_ID" == "logout" ]]; then
  compare_logout_outputs
else
  # compare all
  compare_login_outputs
  compare_withdrawal_outputs
  compare_transfer_outputs
  compare_paybill_outputs
  compare_changeplan_outputs
  compare_disable_outputs
  compare_logout_outputs
fi
