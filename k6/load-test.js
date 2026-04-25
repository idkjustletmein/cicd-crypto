import http from 'k6/http';
import { check, sleep } from 'k6';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

const BASE_URL = __ENV.TARGET_URL || 'https://cryptolab-sxo4.onrender.com';

// Random helper
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Random sleep (real users ≠ robots)
function thinkTime() {
  sleep(Math.random() * 2 + 0.5); // 0.5s → 2.5s
}

// Random test data
function randomPayload() {
  const texts = ['HELLO', 'SECURITY', 'CRYPTO', 'TEST123', 'K6LOAD'];
  const keys = ['1', '3', '5', '7'];

  return JSON.stringify({
    cipher: 'caesar',
    plaintext: texts[randomInt(0, texts.length - 1)],
    key: keys[randomInt(0, keys.length - 1)],
  });
}

export const options = {
  scenarios: {
    browsing_users: {
      executor: 'ramping-vus',
      startVUs: 5,
      stages: [
        { duration: '1m', target: 20 },
        { duration: '2m', target: 50 },
        { duration: '2m', target: 50 },
        { duration: '1m', target: 0 },
      ],
    },

    api_users: {
      executor: 'constant-vus',
      vus: 20,
      duration: '5m',
    },
  },

  thresholds: {
    http_req_duration: ['p(95)<1000'], // stricter now
    http_req_failed: ['rate<0.02'],    // max 2% errors
  },
};

// ── Scenario 1: Browsing behavior ──
export function browsing_users() {
  let homeRes = http.get(`${BASE_URL}/`);

  let csrfToken = '';
  if (homeRes.cookies.csrftoken) {
    csrfToken = homeRes.cookies.csrftoken[0].value;
  }

  check(homeRes, {
    'Home OK': (r) => r.status === 200,
    'Home has CryptoLab': (r) => r.body.includes('CryptoLab'),
  });

  thinkTime();

  // Random navigation path
  if (Math.random() > 0.5) {
    let learnRes = http.get(`${BASE_URL}/learn/`);
    check(learnRes, { 'Learn OK': (r) => r.status === 200 });
  } else {
    let aboutRes = http.get(`${BASE_URL}/about/`);
    check(aboutRes, { 'About OK': (r) => r.status === 200 });
  }

  thinkTime();

  // 70% of users use the API
  if (Math.random() < 0.7) {
    let res = http.post(`${BASE_URL}/encrypt/`, randomPayload(), {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
    });

    check(res, {
      'Encrypt OK': (r) => r.status === 200,
      'Encrypt has result': (r) => {
        try {
          return JSON.parse(r.body).result !== undefined;
        } catch (e) {
          return false;
        }
      },
    });
  }

  thinkTime();
}

// ── Scenario 2: API-heavy users ──
export function api_users() {
  let res = http.post(`${BASE_URL}/encrypt/`, randomPayload(), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'API OK': (r) => r.status === 200,
    'API has result': (r) => {
      try {
        return JSON.parse(r.body).result !== undefined;
      } catch (e) {
        return false;
      }
    },
  });

  sleep(Math.random()); // short delay
}

// ── Report ──
export function handleSummary(data) {
  return {
    "summary.html": htmlReport(data),
    "summary.json": JSON.stringify(data),
  };
}
