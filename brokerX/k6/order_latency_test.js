import http from 'k6/http';
import { check, sleep } from 'k6';

/**
 * Tests the latency for POST requests on the /order endpoint. The setup function initializes client
 * and adds their tokens to a pool so the users in the test refer to user of these accounts. 
 * Allows to determine throughput as well as P50, P90 and P95 on this endpoint. 
 */
const BASE_URL = 'http://broker-app:8000';
let tokens = [];

export function setup() {
  for (let i = 0; i < 10; i++) {
    const email = postClient();
    const token = getJWTToken(email);
    postPasscode(token)
    postWallet(token)
    tokens.push({ email, token });
  }

  return tokens;
}

// Function to simulate actions using the JWT token (e.g., placing orders, adding funds)
function simulateActions(token) {
  postorder(token)
}

let tokenIndex = 0;

export default function (tokens) {
  const token = tokens[tokenIndex];
  tokenIndex = (tokenIndex + 1) % tokens.length;
  simulateActions(token);
  sleep(1);
}