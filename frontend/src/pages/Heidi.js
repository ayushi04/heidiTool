import React, { useState, useEffect } from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import { useLocation } from 'react-router-dom';
import Select from 'react-select';
import { fetchColumns } from '../api';
import OrderingAlgorithmSelect from '../components/OrderingAlgorithmSelect'; // Import the new component
import SelectedDimensions from '../components/SelectedDimensions';
import OrderingDimensions from '../components/OrderingDimensions';
import { getImage } from '../api'; // Import the API function

const Heidi = () => {
  // State
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const datasetPath = searchParams.get('datasetPath');
  
  const [allPossibleDimensions, setAllPossibleDimensions] = useState([]);

  const [imageSrc, setImageSrc] = useState(null);
  const [result, setResult] = useState(null);
  const [selectedDimensions, setSelectedDimensions] = useState([]);
  const [selectedOrderingAlgorithm, setSelectedOrderingAlgorithm] = useState('');
  const [selectedOrderingDimensions, setSelectedOrderingDimensions] = useState([]);

  // Effect for fetching column data
  useEffect(() => {
    const loadColumns = async () => {
      try {
        const fetchedColumns = await fetchColumns(datasetPath);
        setAllPossibleDimensions(fetchedColumns.columns);
      } catch (error) {
        console.error('Error fetching columns:', error.message);
      }
    };
    loadColumns();
  }, [datasetPath]);

  const handleAlgorithmChange = (algorithm) => {
    setSelectedOrderingAlgorithm(algorithm);
  };

  const handleDimensionsChange = (dimensions) => {
    setSelectedDimensions(dimensions);
  };

  const handleOrderingDimensionsChange = (dimensions) => {
    setSelectedOrderingDimensions(dimensions);
  }

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Selected Dimensions:', selectedDimensions);
    console.log('Selected Ordering Algorithm:', selectedOrderingAlgorithm);
    console.log('Selected Ordering Dimensions:', selectedOrderingDimensions);
    try {
      const result = await getImage(datasetPath, selectedOrderingAlgorithm, selectedOrderingDimensions, selectedDimensions);
      setResult(result);
      // Handle the API response, e.g., display a success message
      if (result.status === 'success') {
        console.log('Image fetched successfully:', result);
        const imgData = result.consolidated_image.data;
        const contentType = result.consolidated_image.content_type;

        // Create a data URL with the decoded base64 image data
        const dataUrl = `data:${contentType};base64,${imgData}`;

        // Set the data URL as the image source
        // setImageSrc(dataUrl);
        setImageSrc(dataUrl);
      } else {
        // Handle other cases
        console.error('Error fetching image for dataset: ', datasetPath, ' with ordering algorithm: ', selectedOrderingAlgorithm, ' and ordering dimensions: ', selectedOrderingDimensions);
        console.error('Error: ', result.error);
      }
    } catch (error) {
      // Handle API request errors, e.g., display an error message
      console.error('Error fetching image for dataset: ', datasetPath, ' with ordering algorithm: ', selectedOrderingAlgorithm, ' and ordering dimensions: ', selectedOrderingDimensions);
      console.error('Error: ', error);
    }
  };

  return (
    <Container fluid>
      <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'stretch', height: '100%' }}>
        <div style={{ flex: '0 0 20%' }}>
          {/* Placeholder for the first column */}
        </div>
        <div style={{ flex: '0 0 30%', marginTop: 'auto', marginRight: '20px' }}>
           <OrderingAlgorithmSelect onOrderingAlgorithmChange={handleAlgorithmChange} />
        </div>
        <div style={{ flex: '0 0 30%', marginTop: 'auto' }}>
          <OrderingDimensions allPossibleDimensions={allPossibleDimensions} onOrderingDimensionsChange={handleOrderingDimensionsChange} />
        </div>
        <div style={{ flex: '0 0 20%', marginTop: 'auto', textAlign: 'right' }}>
          <Button variant="primary" type="submit" onClick={handleSubmit}>
            Submit
          </Button>
        </div>
      </div>
      <div style={{ display: 'flex',  flexDirection: 'row', marginTop: '50px' }}>
        <div style={{ flex: '0 0 20%' }}>
          <SelectedDimensions allPossibleDimensions={allPossibleDimensions} onSelectedDimensionsChange={handleDimensionsChange} />
        </div>
        <div style={{ flex: '0 0 80%' }}>
          <div style={{ flex: '1', marginRight: '10px' }}>
            {result && result.status === 'success' ? (
              <img src={imageSrc} alt="Image" />
            ) : (
              <p>No image available. Please select options and submit.</p>
            )
            }
          </div>
          <div style={{ flex: '1' }}>
            {imageSrc && imageSrc.status === 'success' ? (
              <p>{imageSrc.legend}</p>
            ) : null}
          </div>
        </div>
      </div>
    </Container>
  );
};

export default Heidi;
