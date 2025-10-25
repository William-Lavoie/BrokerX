import { postClient, getClient, getWallet, getOrder, postWallet, postOrder, getJWTToken, postPasscode } from './endpoints.js';
import { sleep } from 'k6';

/**
 * General stress test, used to determine the maximum number of concurent users the application
 * can process. Can also be useful to determine average latency. Calls are weighted 2/1 for GET
 * as those are expected to happen more often that POST. In each loop every GET is called twice
 * and each POST once.
 */

export const options = {
  stages: [
    { duration: '15s', target: 150 },
    { duration: '1m', target: 150 }
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],
  },
}

let tokens = [];

export function setup() {
  for (let i = 0; i < 100; i++) {
    const email = postClient();
    const token = getJWTToken(email);
    postPasscode(token)
    postWallet(token, 300.00);
    tokens.push(token);
  }

  return tokens;
}

function simulateClientActions(token) {
  getClient(token);
  getWallet(token);
  getOrder(token);
  postWallet(token, 1.00);
  postOrder(token);
  getClient(token);
  getWallet(token);
  getOrder(token);
}

let tokenIndex = 0;

export default function (tokens) {
  const token = tokens[tokenIndex];
  tokenIndex = (tokenIndex + 1) % tokens.length;
  simulateClientActions(token);
  sleep(1);
}
