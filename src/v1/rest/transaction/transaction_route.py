from .transaction_controller import TransactionPayment, AdminTransactionPayment, AdminTransactionApproval


class TransactionRouter:
    def __init__(self, api):
        api.add_resource(TransactionPayment, '/transaction')
        api.add_resource(AdminTransactionPayment, '/transaction/<user_id>')
        api.add_resource(AdminTransactionApproval, '/transaction/status/<transaction_id>')