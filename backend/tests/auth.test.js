const request = require('supertest');
const mongoose = require('mongoose');
const app = require('../src/app');
const User = require('../src/models/User');

describe('Authentication API Endpoints', () => {
  const testUser = {
    name: 'Ramesh Patel',
    email: 'ramesh.farmer@example.com',
    password: 'SecurePassword123!',
    phone: '+91 98765 43210'
  };

  beforeAll(async () => {
    // If no real mongo connection in CI/test, use memory or mock if available
    const mongoUri = process.env.MONGO_URI || 'mongodb://localhost:27017/ai_agrivision_test';
    try {
      await mongoose.connect(mongoUri, { serverSelectionTimeoutMS: 2000 });
      await User.deleteMany({ email: testUser.email.toLowerCase() });
    } catch (e) {
      // If Mongo server is not running locally, skip database operations gracefully
    }
  });

  afterAll(async () => {
    try {
      await User.deleteMany({ email: testUser.email.toLowerCase() });
      await mongoose.connection.close();
    } catch (e) {}
  });

  describe('POST /api/v1/auth/register', () => {
    it('should reject registration if email is missing', async () => {
      const res = await request(app)
        .post('/api/v1/auth/register')
        .send({ name: 'Farmer John', password: 'password123' });

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('MISSING_FIELDS');
    });

    it('should reject password less than 6 characters', async () => {
      const res = await request(app)
        .post('/api/v1/auth/register')
        .send({ name: 'Farmer John', email: 'john@example.com', password: '123' });

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('INVALID_PASSWORD');
    });
  });

  describe('POST /api/v1/auth/login', () => {
    it('should reject login if credentials missing', async () => {
      const res = await request(app)
        .post('/api/v1/auth/login')
        .send({});

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('MISSING_CREDENTIALS');
    });
  });

  describe('GET /api/v1/auth/me', () => {
    it('should reject access without Bearer token', async () => {
      const res = await request(app).get('/api/v1/auth/me');

      expect(res.status).toBe(401);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });
  });
});
