# **Demo Guide: Phase 3**

## **1. Create an account**
1. Navigate to the root page `/`. Since you are not logged in, you will be redirected to `/login`.
2. Click on the link at the bottom to go to the account creation page (`/create_user`).
3. Enter your information.
4. Click "Submit". If any of the information your entered is not correct, you will be notified.
5. You will be redirected to `/login`.


## **2. Login and verify your passcode**
1. Enter your login information (email and password).
2. Click on Sign in.
3. You will be redirected to `/create_account/validate_passcode`. Note that there might be a delay since you are first redirected to `/`.
4. A passcode has been sent to you by email, however since no SMTP server is configured at the moment, the passcode is sent through logs.
   Please look at `BrokerX\client_service\logs/client_logs` to know your passcode. You can also request a new one.
4. Enter your passcode.
5. You will be redirected to `/`.

## **3. Add funds to your wallet**
1. In the navbar, click on "Wallet".
2. Your current balance will be shown. It should be 0$.
3. Enter the amount you wish to add.
4. Click on "submit"
5. The amount is automatically increased. Note that there is a 10,000$ limit on wallets.
Please note that since the payment system is simulated, you can always withdraw at most 1000$ at a time, however specific value (10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0) trigger errors as a way to tests potential errors coming from the external payment service.


## **4. Subscribe to market data**
1. Enter the symbol for which you wish to subscribe to market data in the searchbar in the navbar. By default AAPL and XEQT are present in the database so you can try those.
2. Click on search
3. You should be redirected to the

## **5. Place Order**
1. Click on Place Order in the navbar.
2. You should be redirected to `/place_order`.
3. Enter the information
4. Click on submit
5. The order should appear below.

Note that if you select Limit and/or GTD in the duration input, additional input fields will appear.

## **6. Modification/Cancellation of orders
1. Navigate to`/place_order` if you are not already there from step 5.
2. Create an order if you do not have one.
3. Click on Edit.
4. Enter the new information.
5. Click on Submit.
6. You should now see the new order.
7. Press on Delete
8. You should no longer see the order

You can create an order using the symbol XEQT to make sure that it won't be executed before you can modify it.

## **7. Execution of order**
This UC does not have a test guide, it should automatically occur when you do step 5.
Use AAPL as it is the only symbol with pre set orders in the database.

Confirm that the information has been updatedin the wallet page, order page and portfolio page.

## **8. Notification of execution**

This UC is not yet functional, but Ihope to get it done by the final deadline.

## **Additional Notes**
- Your session will remain active until you log out manually or the session expires.
- If any redirect fails, please manually navigate to the specified page.