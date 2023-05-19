from accounts.models import Account, EndOfMonthStatement
from payments.models import PaymentReceipt


def create_statement(account_id):
    account = Account.objects.get(pk=account_id)
    receipts = PaymentReceipt.objects.filter(account__pk=account_id)

    total_spent = 0
    total_paid = 0
    for receipt in receipts:
        total_spent += receipt.required_amount
        total_paid += receipt.paid_amount

    outstanding = total_spent - total_paid

    return EndOfMonthStatement.objects.create(
        account=account,
        total_spent=total_spent,
        total_paid=total_paid,
        outstanding=outstanding
    )