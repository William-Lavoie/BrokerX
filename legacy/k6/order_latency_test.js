import { sleep } from 'k6';
import { postClient, postWallet, postOrder, getJWTToken, postPasscode } from './endpoints.js';

/**
 * Tests the latency for POST requests on the /order endpoint. The setup function initializes client
 * and adds their tokens to a pool so the users in the test refer to user of these accounts.
 * Allows to determine throughput as well as P50, P90 and P95 on this endpoint.
 */
let tokens = [];

export const options = {
  stages: [
    { duration: '30s', target: 170 },
    { duration: '1m', target: 170 }
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
  },
}

export function setup() {
  for (let i = 0; i < 50; i++) {
    const email = postClient();
    const token = getJWTToken(email);
    postPasscode(token)
    postWallet(token, 500.00)
    tokens.push(token);
  }

  return tokens;
}

// Function to simulate actions using the JWT token (e.g., placing orders, adding funds)
function simulateActions(token) {
  postOrder(token)
  postOrder(token)
  postOrder(token)
  postOrder(token)
}

let tokenIndex = 0;

export default function (tokens) {
  const token = tokens[tokenIndex];
  tokenIndex = (tokenIndex + 1) % tokens.length;
  simulateActions(token);
  sleep(1);
}