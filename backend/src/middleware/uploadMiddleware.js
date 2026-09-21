const multer = require('multer');
const path = require('path');

// Store file in memory buffer so it can be streamed to Cloudinary and forwarded to ML API
const storage = multer.memoryStorage();

const allowedMimeTypes = [
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/jpg',
  'image/x-webp',
  'image/pjpeg',
  'image/x-png'
];

const allowedExtensions = ['.jpg', '.jpeg', '.png', '.webp'];

const fileFilter = (req, file, cb) => {
  const ext = path.extname(file.originalname || '').toLowerCase();
  const mime = (file.mimetype || '').toLowerCase();

  const isMimeAllowed = allowedMimeTypes.includes(mime);
  const isExtAllowed = allowedExtensions.includes(ext);

  // If MIME is valid or if client/browser transmitted generic octet-stream with valid image extension
  if (isMimeAllowed || (isExtAllowed && (!mime || mime === 'application/octet-stream'))) {
    // Normalize mimetype if missing or generic octet-stream
    if (mime === 'application/octet-stream' || !mime) {
      if (ext === '.webp') file.mimetype = 'image/webp';
      else if (ext === '.png') file.mimetype = 'image/png';
      else file.mimetype = 'image/jpeg';
    }
    cb(null, true);
  } else {
    const error = new Error('Invalid file format. Only JPEG, PNG, and WEBP are supported.');
    error.code = 'UNSUPPORTED_IMAGE_FORMAT';
    cb(error, false);
  }
};

const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10 MB maximum
  },
  fileFilter
});

module.exports = upload;
