# **Demo Guide: Phase 1**

This demo guide concerns UC01, UC02 and UC03. There is no seed data since the application is very simple at this point
and there are no transactions between users.

## **1. Create an account**
1. Navigate to the root page `/`. Since you are not logged in, you will be redirected to `/login`.
2. Click on the link at the bottom to go to the account creation page (`/create_user`).
3. Enter your information. Note that *Preferred communication method* is currently not operational and *email* will be chosen despite what you pick.
4. Click "Submit". If any of the information your entered is not correct, you will be notified.

## **2. Verify your passcode**
1. You should have been redirected to `confirm_passcode`.
2. A passcode has been sent to you by email, however since no SMTP server is configured at the moment, the passcode is sent through logs.
   Please look at `BrokerX\brokerX\django.error_logs` to know your passcode.
3. Enter your passcode.
4. You will be redirected to `/`.


## **3. Add funds to your wallet**
1. In the navbar, click on "Wallet".
2. Your current balance will be shown. It should be 0$.
3. Enter the amount you wish to add.
4. Click on "submit"
5. The amount is automatically increased. Note that there is a 10,000$ limit on wallets.
Please note that since the payment system is simulated, you can always withdraw at most 1000$ at a time, however specific value (10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0) trigger errors as a way to tests potential errors coming from the external payment service.

## **Additional Notes**
- Your session will remain active until you log out manually or the session expires.
