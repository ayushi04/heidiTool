// api.js
const API_BASE_URL = 'http://localhost:8080'; // Replace with your actual API URL

export const uploadFile = async (file, fixMethod) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fix', fixMethod);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      // Handle successful response
      return await response.json();
    } else {
      // Handle error response
      throw new Error('Upload failed');
    }
  } catch (error) {
    // Handle network or other errors
    throw error;
  }
};
