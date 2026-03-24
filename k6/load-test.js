import http from 'k6/http';
import { check, sleep } from 'k6';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

// ── Configuration ──────────────────────────────────────────────
const BASE_URL = __ENV.TARGET_URL || 'https://cryptolab-sxo4.onrender.com';

export const options = {
  stages: [
    // Stage 1: Smoke test — baseline sanity
    { duration: '30s', target: 1 },
    // Stage 2: Load test — ramp to 10 VUs
    { duration: '1m',  target: 10 },
    // Stage 3: Cooldown — graceful ramp-down
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],  // 95% of requests under 2s
    http_req_failed:   ['rate<0.05'],   // Error rate under 5%
  },
};

// ── Test Scenarios ─────────────────────────────────────────────
export default function () {
  // 1. Home page
  let homeRes = http.get(`${BASE_URL}/`);
  
  // Extract the CSRF Token cookie that Django sets
  let csrfToken = '';
  if (homeRes.cookies.csrftoken && homeRes.cookies.csrftoken.length > 0) {
    csrfToken = homeRes.cookies.csrftoken[0].value;
  }

  check(homeRes, {
    'Home: status 200': (r) => r.status === 200,
    'Home: has CryptoLab': (r) => r.body.includes('CryptoLab'),
  });

  sleep(1);

  // 2. Learn page
  let learnRes = http.get(`${BASE_URL}/learn/`);
  check(learnRes, {
    'Learn: status 200': (r) => r.status === 200,
  });

  sleep(1);

  // 3. About page
  let aboutRes = http.get(`${BASE_URL}/about/`);
  check(aboutRes, {
    'About: status 200': (r) => r.status === 200,
  });

  sleep(1);

  // 4. Encrypt API — Caesar cipher
  let encryptPayload = JSON.stringify({
    cipher: 'caesar',
    plaintext: 'HELLO WORLD',
    key: '3',
  });

  let encryptRes = http.post(`${BASE_URL}/encrypt/`, encryptPayload, {
    headers: { 
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken  // Pass the extracted token to bypass Forbidden checks
    },
  });

  check(encryptRes, {
    'Encrypt: status 200': (r) => r.status === 200,
    'Encrypt: has result': (r) => {
      try {
        return JSON.parse(r.body).result !== undefined;
      } catch (e) {
        return false;
      }
    },
  });

  sleep(1);
}

export function handleSummary(data) {
  return {
    "summary.html": htmlReport(data),
    "summary.json": JSON.stringify(data), // We can optionally keep JSON just in case
  };
}
