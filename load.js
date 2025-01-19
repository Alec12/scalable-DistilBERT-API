import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const target = 10;
export const options = {
  stages: [
    { duration: '30s', target: target }, // simulate ramp-up of traffic from 0 to target users.
    { duration: '7m', target: target }, // stay at 10 users
    { duration: '3m', target: 0 }, // ramp-down to 0 users
  ],
  thresholds: {
    'http_req_duration': ['p(99)<2000'] // 99% of requests must complete below 2s
  },
};

const fixed = ["I love you!", "I hate you!", "I am a Kubernetes Cluster!"]
var random_shuffler = [
  "I love you!",
  "I hate you!",
  "I am a Kubernetes Cluster!",
  "I ran to the store",
  "The students are very good in this class",
  "Working on Saturday morning is brutal",
  "How much wood could a wood chuck chuck if a wood chuck could chuck wood?",
  "A Wood chuck would chuck as much wood as a wood chuck could chuck if a wood chuck could chuck wood",
  "Food is very tasty",
  "Welcome to the thunderdome"
];

const generator = (cacheRate) => {
  const rand = Math.random()
  const text = rand > cacheRate
    ? random_shuffler.map(value => ({ value, sort: Math.random() }))
      .sort((a, b) => a.sort - b.sort)
      .map(({ value }) => value)
    : fixed
  return {
    text
  }
}

const NAMESPACE = __ENV.NAMESPACE
const BASE_URL = `https://${NAMESPACE}.mids255.com`;
const CACHE_RATE = .95

export default () => {
  const payload = JSON.stringify(generator(CACHE_RATE))
  const predictionRes = http.request('POST', `${BASE_URL}/project/bulk-predict`, payload)
  check(predictionRes, {
    'is 200': (r) => r.status === 200
  })
};
