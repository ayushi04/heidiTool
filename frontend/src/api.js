import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080'; // Replace with your actual API URL

export const uploadFile = async (file, fixMethod) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fix', fixMethod);

    const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.status === 200) {
      // Handle successful response
      return response.data;
    } else {
      // Handle error response
      throw new Error('Upload failed');
    }
  } catch (error) {
    // Handle network or other errors
    throw error;
  }
};

export const fetchColumns = async (datasetPath) => {
  const response = await axios.get(`${API_BASE_URL}/heidi/columns?datasetPath=${datasetPath}`, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  if (response.status === 200) {
    // Handle successful response
    return response.data;
  } else {
    // Handle error response
    throw new Error('Upload failed');
  }
  
};

export const getImage = async (datasetPath, orderingAlgorithm, orderingDimensions) => {
  const response = await axios.get(`${API_BASE_URL}/heidi/image?datasetPath=${datasetPath}&orderingAlgorithm=${orderingAlgorithm}&orderingDimensions=${orderingDimensions}`, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  if (response.status === 200) {
    // Handle successful response
    return response.data;
  } else {
    // Handle error response
    throw new Error('Upload failed');
  }
  
}

