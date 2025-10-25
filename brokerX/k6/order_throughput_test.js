import http from 'k6/http';
import { check, sleep } from 'k6';
import { uuid } from 'k6';

// Variables (You can modify based on environment variables or config)
const BASE_URL = 'http://broker-app:8000'; // Replace with your actual API URL
const NUM_CLIENTS = 10; // Total number of clients to simulate
const NUM_REQUESTS = 100; // Total number of requests, distributed among clients
const JWT_TOKENS = []; // Array to store tokens for each client

// Function to create a new client
function createClient() {
  const randomNumber = Math.floor(Math.random() * 100000000); // Generates a number from 0 to 99,999,999
  const randomEmail = `john.doe${randomNumber.toString().padStart(8, '0')}@example.com`;  // Ensure 8 digits

   const randomPhone = Math.floor(Math.random() * 100000000); // Generates a number from 0 to 99,999,999
     const randomPhonenumber = randomPhone.toString().padStart(9, '0')

  const payload = JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    address: '123 Main St',
    date_of_birth: '1990-01-01',
    email: randomEmail,
    phone_number: randomPhonenumber,
    password: 'strongpassword123',
  });

  const res = http.post(`${BASE_URL}/client`, payload, { headers: { 'Content-Type': 'application/json' } });
  check(res, { 'Client created successfully': (r) => r.status === 201 });

  return randomEmail; // Assuming the response contains client info, including an ID or something to identify the user
}

// Function to verify passcode for the client
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

// Function to simulate getting a JWT token for the client after passcode verification
function getJWTToken(email) {
  // In a real scenario, we'd extract the token from the response of the `/passcode` verification
  const res = http.post(`${BASE_URL}/api/token/`, JSON.stringify({username: email, password: "TBD"}), { headers : {
    'Content-Type': 'application/json',
  }});
  check(res, { 'Token verified successfully': (r) => r.status === 200 });
 // Mocking the JWT token for test purposes
  return res.json().access;
}

// Function to simulate client activity after obtaining the JWT token (e.g., adding funds, placing orders)
function simulateClientActions(jwtToken) {
  const headers = {
    'Authorization': `Bearer ${jwtToken}`,
    'Content-Type': 'application/json',
    'Idempotency-Key': generateUUID(),
  };

  // Add funds (example)
  const addFundsPayload = JSON.stringify({ amount: 1000.00 });
  const resAddFunds = http.post(`${BASE_URL}/wallet`, addFundsPayload, { headers });
  check(resAddFunds, { 'Funds added successfully': (r) => r.status === 201 || r.status === 200 });

  // Place an order (example)
  const placeOrderPayload = JSON.stringify({
    direction: 'buy',
    quantity: 10,
    symbol: 'AAPL',
    limit: 10.00,
    'Idempotency-Key': generateUUID(),
  });
  const resPlaceOrder = http.post(`${BASE_URL}/order`, placeOrderPayload, { headers });
  const getPlaceOrder = http.get(`${BASE_URL}/order`, {
    headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
    }
});
http.get(`${BASE_URL}/client`, {
    headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
    }
});
http.get(`${BASE_URL}/wallet`, {
    headers: {
        'Authorization': `Bearer ${jwtToken}`,
        'Content-Type': 'application/json'
    }
});

  check(resPlaceOrder, { 'Order placed successfully': (r) => r.status === 201 });
}

// Main test function
export default function () {
  let clientId;

  // Step 1: Create a client
  const email = createClient();
  const jwtToken = getJWTToken(email);

  // Step 2: Verify passcode
  const passcodeResponse = verifyPasscode(jwtToken);

  // Step 3: Get JWT token after passcode verification (simulate this)

  // Store the token for future use (optional)
  JWT_TOKENS.push(jwtToken);

  // Step 4: Simulate client actions with the obtained JWT token
  simulateClientActions(jwtToken);

  sleep(1); // Add a sleep period to simulate realistic behavior
}


function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
