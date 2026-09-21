const request = require('supertest');
const app = require('../src/app');

describe('Prediction API Endpoints', () => {
  describe('POST /api/v1/predictions', () => {
    it('should reject unauthenticated prediction requests with 401', async () => {
      const res = await request(app)
        .post('/api/v1/predictions')
        .attach('image', Buffer.from('fake image content'), 'test.jpg');

      expect(res.status).toBe(401);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });
  });

  describe('GET /api/v1/predictions', () => {
    it('should reject unauthenticated history query with 401', async () => {
      const res = await request(app).get('/api/v1/predictions');

      expect(res.status).toBe(401);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('UNAUTHORIZED');
    });
  });
});
