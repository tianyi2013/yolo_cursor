import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const processImage = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_BASE_URL}/process-image/`, formData);
  return response.data;
};

export const getDownloadUrl = (requestId, filename) => 
  `${API_BASE_URL}/download/${requestId}/${filename}`;

export const cleanupRequest = async (requestId) => {
  await axios.delete(`${API_BASE_URL}/cleanup/${requestId}`);
}; 