# UC-03 – Adding funds to the wallet (virtual deposit)

## Objective
Allow clients to add funds to their digital wallet through simulated deposits to have the required liquidity to place buy orders. This ensures the availability of funds for market transactions.

## Primary Actor
Client

## Secondary Actors
   - Simulated payment service
   - Back-Office
## Trigger
The client deposits fiat money into their virtual wallet.

## Preconditions
The client possesses an active account.

## Postconditions
- **Success:**
    - The client's wallet has been credited and its balance has been updated.
    - The deposit has been logged.
- **Failure:** The wallet's balance does not change.

## Main Scenario (Success Path)
1. The client enters the amount they wish to deposit.
2. The system validates that the amount is within the permitted limits for the account and an anti-fraud check is executed.
3. The system creates a *"Pending"* transaction.
4. The simulated payment service processes the transaction and returns a *"Settled"* response.
5. The money is added to the client's wallet, the client is notified that the deposit was successful, and the system logs the transaction, including the timestamp, device, amount, and status.

## Alternative Flows
- **A1 – [The transaction is asynchronous]:** A message explaining that the transaction is being executed is displayed to the client. When it is resolved, the transaction is updated with its current state and the client is notified through email or SMS (according to the preferences) that the transaction was either successful or unsuccessful, with an explanatory message in the latter case.

## Exception Scenarios
- **E1 – [The Simulated payment service denies the transaction]:** The transaction is set to *"Rejected*" and an explanatory message is displayed to the client.
- **E2 – [The transaction has the same idempotency-key as an existing one]:** The current transaction is set to *"Cancelled"* and the result of the existing one is displayed. The amount in the wallet does not change.

## Priority (MoSCoW)
`Must` Clients cannot make transactions without funds, allowing them to deposit money into their digital wallets is therefore a high priority.