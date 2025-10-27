import json
from decimal import Decimal


class MockPaymentService:
    def withdraw_funds(self, email: str, amount: Decimal) -> str:

        # Simulate different errors based on the exact amount requested
        if amount == Decimal("10.00"):
            raise TimeoutError("Request timed out while withdrawing funds.")

        elif amount == Decimal("20.00"):
            raise ConnectionError("Network connection error occurred.")

        elif amount == Decimal("30.00"):
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "code": 503,
                    "message": "Unauthorized access.",
                }
            )

        elif amount == Decimal("40.00"):
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "message": "Rate limit exceeded.",
                }
            )

        elif amount == Decimal("50.00"):
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "code": 500,
                    "message": "Internal server error.",
                }
            )

        elif amount == Decimal("60.00"):
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "message": "Invalid withdrawal amount.",
                }
            )

        elif amount == Decimal("70.00"):
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "code": 503,
                    "message": "Account is locked.",
                }
            )

        # Regular validation & response
        elif amount < 0:
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "code": 400,
                    "message": "The amount to withdraw must be positive.",
                }
            )

        elif amount == 0:
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "code": 400,
                    "message": "Cannot withdraw zero amount.",
                }
            )

        elif amount > 1000.00:
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "code": 400,
                    "message": "Insufficient funds.",
                }
            )

        return json.dumps(
            {
                "success": True,
                "balance": 1000.00,
                "code": 200,
                "message": f"Withdrawal of {float(amount):.2f} successful.",
            }
        )
