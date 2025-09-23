from decimal import Decimal
import json


class MockPaymentService:
    def withdraw_funds(self, email: str, amount: Decimal) -> str:
        if not isinstance(amount, Decimal):
            raise TypeError("amount must be a Decimal")

        # Simulate different errors based on the exact amount requested
        elif amount == Decimal("10.00"):
            raise TimeoutError("Request timed out while withdrawing funds.")

        elif amount == Decimal("20.00"):
            raise ConnectionError("Network connection error occurred.")

        elif amount == Decimal("30.00"):
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
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
                    "message": "Account is locked.",
                }
            )

        # Regular validation & response
        elif amount < 0:
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "message": "The amount to withdraw must be positive.",
                }
            )

        elif amount == 0:
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "message": "Cannot withdraw zero amount.",
                }
            )

        elif amount > 1000.00:
            return json.dumps(
                {
                    "success": False,
                    "balance": 1000.00,
                    "message": "Insufficient funds.",
                }
            )

        return json.dumps(
            {
                "success": True,
                "balance": 1000.00,
                "message": f"Withdrawal of {float(amount):.2f} successful.",
            }
        )
