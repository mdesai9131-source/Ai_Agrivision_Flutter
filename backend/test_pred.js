const fs = require('fs');
const axios = require('./node_modules/axios');
const FormData = require('./node_modules/form-data');

async function run() {
  try {
    console.log('1. Registering or logging in test user...');
    let token = '';
    const email = 'farmer_pred_test@agrivision.com';
    const password = 'Password123!';
    try {
      const regRes = await axios.post('http://127.0.0.1:5000/api/v1/auth/register', {
        name: 'Farmer Test',
        email,
        password,
        phone: '9876543210'
      });
      token = regRes.data.data.token;
      console.log('Registered successfully! Token received.');
    } catch (e) {
      if (e.response && e.response.data && e.response.data.error && e.response.data.error.code === 'USER_EXISTS') {
        const loginRes = await axios.post('http://127.0.0.1:5000/api/v1/auth/login', {
          email,
          password
        });
        token = loginRes.data.data.token;
        console.log('Logged in successfully! Token received.');
      } else {
        throw e;
      }
    }

    console.log('2. Sending prediction request for Wheat...');
    const imagePath = 'd:/Projects/Ai-Agrivision/frontend/assets/images/sample_leaf.jpg';
    const form = new FormData();
    form.append('image', fs.createReadStream(imagePath), {
      filename: 'sample_wheat_leaf.jpg',
      contentType: 'image/jpeg'
    });
    form.append('crop', 'Wheat');
    form.append('latitude', '23.2599');
    form.append('longitude', '77.4126');

    const predRes = await axios.post('http://127.0.0.1:5000/api/v1/predictions', form, {
      headers: {
        ...form.getHeaders(),
        Authorization: `Bearer ${token}`
      }
    });

    console.log('Prediction Response Status:', predRes.status);
    console.log('Prediction Data:', JSON.stringify(predRes.data, null, 2));
  } catch (err) {
    console.error('Error during test:');
    if (err.response) {
      console.error('Status:', err.response.status);
      console.error('Data:', JSON.stringify(err.response.data, null, 2));
    } else {
      console.error(err.message);
    }
  }
}

run();
