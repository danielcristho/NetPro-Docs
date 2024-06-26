import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';

// Configuration for the test
export let options = {
    stages: [
        { duration: '1s', target: 10 },
        { duration: '1m', target: 10 },
        { duration: '1m', target: 0 },
    ],
    thresholds: {
        'http_req_duration': ['p(95)<500'], // 95% of requests must complete below 500ms
        'http_req_failed{status:200}': ['rate<0.01'], // HTTP errors should be less than 1%
    },
};

export default function () {
    let res = http.get('https://127.0.0.1:8433/');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
    sleep(1)
}
