# AI-AgriVision Backend API

Scalable, production-ready Node.js/Express and MongoDB REST API powering the AI-AgriVision agriculture platform.

---

## Features

- **JWT Authentication & bcrypt Password Hashing**: Secure user access with session tokens and salt-hashed passwords.
- **Image Pipeline**: Memory buffer handling with Multer, Cloudinary CDN streaming, and forwarding to the Python FastAPI ML microservice.
- **MongoDB Persistence**: Mongoose models for Farmers and Predictions with compound indices for fast chronological querying.
- **Nearby Agro Assistance**: Calculates proximity to Krishi Vigyan Kendras, certified seed & fertilizer depots, and agro-advisors using Haversine mathematics.
- **Defense in Depth**: Helmet security headers, CORS origin whitelisting, rate limiting per IP window, and zero stack-trace leakage in production.

---

## API Endpoints

### 1. Authentication (`/api/v1/auth`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/register` | Public | Register farmer account (name, email, password, location) |
| `POST` | `/login` | Public | Authenticate and obtain JWT token |
| `GET` | `/me` | Private | Retrieve authenticated farmer details |

### 2. Crop Disease Predictions (`/api/v1/predictions`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/` | Private | Upload leaf image, get diagnosis, store in DB |
| `GET` | `/` | Private | List previous prediction history (paginated) |
| `GET` | `/:id` | Private | Fetch details of a single diagnosis record |
| `DELETE` | `/:id` | Private | Remove a prediction record |

### 3. Farmer Profile (`/api/v1/users`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/profile` | Private | Fetch farmer profile |
| `PUT` | `/profile` | Private | Update farm coordinates and profile settings |

### 4. Nearby Agro Support (`/api/v1/agro`)
| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/nearby` | Private | Query nearby agriculture shops, KVKs, and experts |

---

## Environment Variables

Create a `.env` file in the root of `backend/`:
```env
PORT=5000
NODE_ENV=development
MONGO_URI=mongodb://localhost:27017/ai_agrivision
JWT_SECRET=your_jwt_secret_key_at_least_32_chars
ML_SERVICE_URL=http://localhost:8000
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
MAPS_API_KEY=your_maps_key
```

---

## Running Locally

```bash
cd backend
npm install
npm run dev
```

Run tests:
```bash
npm test
```
