# UC-01 – Client Registration and Identity Validation

## Objective
Allow new clients to create an account on the platform by providing relevant personal information, validate their identity in accordance with KYC/AML regulations and grant them access to the platform.

## Primary Actor
Client

## Secondary Actors
None

## Trigger
The client requests to create an account.

## Preconditions
None

## Postconditions
- **Success:** The account has been created and put in *"Pending"* state, then transitions to "Active" after it has been validated.
- **Failure:** The account is not created or is set to *"Rejected"* with a reason.

## Main Scenario (Success Path)
1. The client enters required personal information, including:
    - Name
    - Address
    - Date of birth
    - Email
    - Phone number
    - Password: must have at least 8 characters, including at least one uppercase, one lowercase, one number and one special character.
    The client must confirm their password by entering it twice. Both entries must match.
    A visual indicator shows password strength.
    - Preferred communication method (email or SMS)

2. The system validates that the client inputs are correctly formatted, creates a new account in the *"Pending"* state and sends a verification code to the client through email or SMS, according to the client's preference.
3. The client enters the one-time password (OTP) sent via email or SMS to complete the account verification step.
4. The system sets the account to "Active" and logs the account creation event, including the timestamp and unique document identifiers (document fingerprints and/or cryptographic hashes) for auditing.

## Alternative Flows
- **A1 – [Verification code uncompleted]:** The account remains *"Pending"* and the code expires after 10 minutes. The client can request a new OTP. If no OTP is confirmed within 24h, the account is deleted and the client must restart the process from the beginning in order to create an account. The client receives a reminder 1h prior to expiration on their preferred communication method (email or SMS).
- **A2 - [Client inputs are invalid]:** The invalid information is highlighted with an explanation and the client is prompted to try again. No account is created.

## Exception Scenarios
- **E1 – [Duplicate email/phone number]:** The request is rejected and the client is prompted to recover their existing account associated with the email and/or phone number.

## Priority (MoSCoW)
`Must` Without an account, clients cannot access the platform, client registration is therefore a top priority.