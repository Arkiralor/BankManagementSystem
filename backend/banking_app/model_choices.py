class AccountChoice:
    savings = "Savings"
    current = "Current"
    loan = "Loan"
    credit = "Credit"

    ACCOUNT_TYPES = (
        (savings, savings),
        (current, current),
        (loan, loan),
        (credit, credit)
    )

class TransactionChoice:

    cash_deposit = "Cash Deposit"
    account_transfer = "Account Transfer"
    withdrawal = "Account Withdrawal"

    TRANSACTION_TYPE = (
        (cash_deposit, cash_deposit),
        (account_transfer, account_transfer)
    )