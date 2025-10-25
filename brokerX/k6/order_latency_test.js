import http from 'k6/http';
import { check, sleep } from 'k6';

// Configuration variables
const BASE_URL = 'http://broker-app:8000';  // Replace with your actual base URL
let users = [];
// Function to create a user
function createUser() {
  const randomEmail = `user${Math.floor(Math.random() * 100000000)}@example.com`;
  const randomPhone = Math.floor(Math.random() * 100000000);
  const randomPhoneNumber = randomPhone.toString().padStart(9, '0');

  const payload = JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    email: randomEmail,
    address: '123 Main St',
    date_of_birth: '1990-01-01',
    phone_number: randomPhoneNumber,
    password: 'TestPassword123',
  });

  const res = http.post(`${BASE_URL}/client`, payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, { 'User created successfully': (r) => r.status === 201 });

  return { email: randomEmail, password: 'TestPassword123' };
}

function verifyPasscode(token) {
  const payload = JSON.stringify({
    passcode: '123456', // Assuming the passcode is always the same for the test, can be dynamic if needed
  });

  const res = http.post(`${BASE_URL}/passcode`, payload, { headers : {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  } });
  check(res, { 'Passcode verified successfully': (r) => r.status === 200 });

  return res.json(); // Assuming the response contains a JWT token
}

// Function to authenticate the user and get a JWT token
function authenticateUser(user) {
  const loginPayload = JSON.stringify({
    username: user.email,
    password: "TBD",
  });

  const res = http.post(`${BASE_URL}/api/token/`, loginPayload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, { 'Login successful': (r) => r.status === 200 });

  return res.json().access;  // Return the JWT token
}

function addFunds(token) {
    const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Idempotency-Key': generateUUID(),
      };

      // Add funds (example)
      const addFundsPayload = JSON.stringify({ amount: 1000.00 });
      const resAddFunds = http.post(`${BASE_URL}/wallet`, addFundsPayload, { headers });
      check(resAddFunds, { 'Funds added successfully': (r) => r.status === 201 || r.status === 200 });
}

// Setup function to create users
export function setup() {

  // Create 10 users
  for (let i = 0; i < 10; i++) {
    const user = createUser();
    const token = authenticateUser(user);
    verifyPasscode(token)
    addFunds(token)
    users.push({ ...user, token });  // Store user info and JWT token
  }

  return users;  // Return the list of created users and tokens
}

// Function to simulate actions using the JWT token (e.g., placing orders, adding funds)
function simulateActions(jwtToken) {
  const headers = {
    'Authorization': `Bearer ${jwtToken}`,
    'Content-Type': 'application/json',
    'Idempotency-Key': generateUUID(),
  };

  // Place an order (example action)
  const placeOrderPayload = JSON.stringify({
    direction: 'buy',
    quantity: 10,
    symbol: 'AAPL',
    limit: 10.00,
  });
  const resPlaceOrder = http.post(`${BASE_URL}/order`, placeOrderPayload, { headers });
  check(resPlaceOrder, { 'Order placed successfully': (r) => r.status === 201 });
   http.post(`${BASE_URL}/order`, placeOrderPayload, { headers });

}
let userIndex = 0;

export default function (users) {
  // Get the list of users created in setup()

  const user = users[userIndex];
  userIndex = (userIndex + 1) % users.length;
  // Simulate user actions using the JWT token
  simulateActions(user.token);

  sleep(1);  // Add sleep to simulate realistic user behavior
}

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
