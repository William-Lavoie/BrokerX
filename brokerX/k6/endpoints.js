import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = 'http://broker-app:8000'; // Replace with your actual API URL

/**
 * @endpoint /passcode
 * @method POST
 * @param {string} token
 * @returns
 */
export function postPasscode(token) {
  const payload = JSON.stringify({
    passcode: '123456',
  });

  const res = http.post(`${BASE_URL}/passcode`, payload, { headers : {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  } });
  check(res, { 'Passcode verified successfully': (r) => r.status === 200 });
}

/**
 * Retrieves a JWT token for a user
 * @endpoint api/token/
 * @method POST
 * @param {string} email
 * @returns
 */
export function getJWTToken(email) {
  const res = http.post(`${BASE_URL}/api/token/`, JSON.stringify({username: email, password: "TBD"}), { headers : {
    'Content-Type': 'application/json',
  }});
  check(res, { 'Token verified successfully': (r) => r.status === 200 });
  return res.json().access;
}

/**
 * @endpoint /client
 * @method GET
 * @param {string} token
 */
export function getClient(token) {
  http.get(`${BASE_URL}/client`, {
      headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
      }
  });
}

/**
 * Creates a user instance with randomized email and password
 * and returns the email. Note that this does not guarantee uniqueness,
 * however under realistic charges collisions should be very rare.
 * @endpoint /client
 * @method GET
 * @returns email
 */
export function postClient() {
    const randomNumber = Math.floor(Math.random() * 100000000);
    const email = `john.doe${randomNumber.toString().padStart(8, '0')}@example.com`;
    const phoneNumber = randomNumber.toString().padStart(9, '0')

  const payload = JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    address: '123 Main St',
    date_of_birth: '1990-01-01',
    email: email,
    phone_number: phoneNumber,
    password: 'strongpassword123',
  });
    const res = http.post(`${BASE_URL}/client`, payload, { headers: { 'Content-Type': 'application/json' } });
    check(res, { 'Client created successfully': (r) => r.status === 201 });

  return email;
}

/**
 * @endpoint /wallet
 * @method GET
 * @param {string} token
 */
export function getWallet(token) {
  http.get(`${BASE_URL}/wallet`, {
      headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
      }
  });
}

/**
 * @endpoint /wallet
 * @method POST
 * @param {string} token
 */
export function postWallet(token) {
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
    'Idempotency-Key': generateUUID(),
  };

  const addFundsPayload = JSON.stringify({ amount: 1000.00 });
  const resAddFunds = http.post(`${BASE_URL}/wallet`, addFundsPayload, { headers });
  check(resAddFunds, { 'Funds added successfully': (r) => r.status === 201 || r.status === 200 });
}

/**
 * @endpoint /order
 * @method GET
 * @param {string} token
 */
export function getOrder(token) {
  const getPlaceOrder = http.get(`${BASE_URL}/order`, {
      headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
      }
  });
}

/**
 * @endpoint /order
 * @method POST
 * @param {string} token
 */
export function postOrder(token) {
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
    'Idempotency-Key': generateUUID(),
  };

  const placeOrderPayload = JSON.stringify({
    direction: 'buy',
    quantity: 10,
    symbol: 'AAPL',
    limit: 10.00,
  });
  const resPlaceOrder = http.post(`${BASE_URL}/order`, placeOrderPayload, { headers });
  check(resPlaceOrder, { 'Order placed successfully': (r) => r.status === 201 });
}


/**
 * Returns a uuid for idempotency keys
 * @returns {uuid}
 */
export function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}