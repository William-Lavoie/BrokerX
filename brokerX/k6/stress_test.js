import { postClient, getClient, getWallet, getOrder, postWallet, postOrder, getJWTToken, postPasscode } from './endpoints.js';
import { sleep } from 'k6';

/**
 * General stress test, used to determine the maximum number of concurent users the application
 * can process. Can also be useful to determine average latency. Calls are weigthed 2/1 for GET
 * as those are expected to happen more often that POST. In each loop every GET is called twice
 * and each POST once.
 */

const BASE_URL = 'http://broker-app:8000'; // Replace with your actual API URL

export const options = {
  stages: [
    {duration: '2m', target: 300}
  ],
  thresholds: { http_req_failed: ['rate<0.05'] },
}


function simulateClientActions(token) {
  getClient(token);
  getWallet(token);
  getOrder(token);
  postWallet(token);
  postOrder(token);
  getClient(token);
  getWallet(token);
  getOrder(token);
}

export default function () {
  const email = postClient();
  const jwtToken = getJWTToken(email);
  postPasscode(jwtToken);
  simulateClientActions(jwtToken);
  sleep(1);
}
