import React, { useState, useEffect } from 'react';
import { Container, Form, Button } from 'react-bootstrap';
import { useLocation } from 'react-router-dom';
import Select from 'react-select';
import { fetchColumns } from '../api';
import OrderingAlgorithmSelect from './OrderingAlgorithmSelect'; // Import the new component
import SelectedDimensions from './SelectedDimensions';

const Heidi = () => {
  // State
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const datasetPath = searchParams.get('datasetPath');

  const [allPossibleDimensions, setAllPossibleDimensions] = useState([]);
  const [selectedDimensions, setSelectedDimensions] = useState([]);
  const defaultDimensions = allPossibleDimensions.reduce((checkboxes, dimension) => {
    checkboxes[dimension] = false;
    return checkboxes;
  }, {});
  const [dimensionCheckboxes, setDimensionCheckboxes] = useState(defaultDimensions);
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

  // Handle checkbox change
  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    setDimensionCheckboxes({ ...dimensionCheckboxes, [name]: checked });
  };

  const handleAlgorithmChange = (algorithm) => {
    setSelectedOrderingAlgorithm(algorithm);
  };

  const handleDimensionsChange = (dimensions) => {
    setSelectedDimensions(dimensions);
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Selected Dimensions:', selectedDimensions);
    console.log('Selected Ordering Algorithm:', selectedOrderingAlgorithm);
    console.log('Selected Ordering Dimensions:', selectedOrderingDimensions);
  };

  return (
    <Container fluid>
      <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'stretch', height: '100%' }}>
        <div style={{ flex: '0 0 20%' }}>
          {/* Placeholder for the first column */}
        </div>
        <div style={{ flex: '0 0 30%', marginTop: 'auto', marginRight: '20px' }}>
           <OrderingAlgorithmSelect onOrderingAlgorithmChange={handleAlgorithmChange} s/>
        </div>
        <div style={{ flex: '0 0 30%', marginTop: 'auto' }}>
          <Form.Group>
            <Form.Label>Ordering Dimensions</Form.Label>
            <Select
              isMulti
              options={allPossibleDimensions.map((dimension) => ({
                value: dimension,
                label: dimension,
              }))}
              value={selectedOrderingDimensions.map((dimension) => ({
                value: dimension,
                label: dimension,
              }))}
              onChange={(selectedOptions) => setSelectedOrderingDimensions(selectedOptions.map((option) => option.value))}
            />
          </Form.Group>
        </div>
        <div style={{ flex: '0 0 20%', marginTop: 'auto', textAlign: 'right' }}>
          <Button variant="primary" type="submit" onClick={handleSubmit}>
            Submit
          </Button>
        </div>
      </div>
      <div style={{ marginTop: '20px' }}>
        <h4>Dimensions</h4>
          <SelectedDimensions allPossibleDimensions={allPossibleDimensions} onSelectedDimensionsChange={handleDimensionsChange} />
      </div>
    </Container>
  );
};

export default Heidi;
