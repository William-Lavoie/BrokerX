# UC-02 – Authentication and MFA

## Objective
Allow clients to log in securely on the platform with their email and password as well as a multi-factor authentication (MFA) to protect their accounts against unauthorized access.

## Primary Actor
Client

## Secondary Actors
None

## Trigger
The client logs in to the platform.

## Preconditions
The client possesses an active account.

## Postconditions
- **Success:** A session has been established with a token in *Client* mode.
- **Failure:** No session is created.

## Main Scenario (Success Path)
1. The client enters their email and password.
2. The system validates that the account exists and that the password is correct.
3. The client receives a one-time passcode (OTP) by email or SMS, according to their account preferences, as part of the MFA process.
4. The client completes the MFA step by entering their OTP. OTPs are valid for 10 minutes, after which clients are prompted to request a new one.
5. A JWT session token is created and securely stored in a cookie, and the login request is logged for audit purposes, including the timestamp, IP address, device and success code. The token expires automatically after 24h, or on logout.

## Alternative Flows
- **A1 – [The client is using a known device]:** If the client has previously logged on to the platform on their current device, the MFA step is omitted, unless the client attempts to perform a sensitive operation such as adding funds to their wallet or placing orders, in which case the client will be prompted to complete the MFA in order to complete the operation. Known devices are identified via local device tokens and valid for 60 days.

## Exception Scenarios
- **E1 – [The MFA fails 3 times]:** The account is set to *"Locked"* for 30 minutes, during which the client cannot access their account. After this period, the client may resume their login attempt or contact customer support.
- **E2 – [More than 5 login attempts are made from the same IP address within 10 minutes]:** The IP is blocked for 30 minutes and the event is logged for security purposes. The client is prompted to contact customer support to appeal this decision.
- **E3 - [The IP address is flagged as a risk]:** The account is set to *"Suspended"*, the client is prompted to contact customer support to prove the account belongs to them.
- **E4 - [The account is suspended]:** The login request is rejected with an explanation. The client is prompted to contact customer support.
- **E5 - [The OTP token is expired]:** The login request is rejected with an explanation. The client is prompted to request a new OTP.

## Priority (MoSCoW)
`Must` Without a proper authentication system, client information is compromised. A safe and reliable authentication system is therefore a high priority.