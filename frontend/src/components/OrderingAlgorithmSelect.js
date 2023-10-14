import React, { useState } from 'react';
import Select from 'react-select';
import { Form } from 'react-bootstrap';

const OrderingAlgorithmSelect = ({ onOrderingAlgorithmChange }) => {
  const [selectedOrderingAlgorithm, setSelectedOrderingAlgorithm] = useState('');

  // Ordering algorithm options
  const allPossibleOrderingAlgorithm = ['Centroid Ordering', 'Option 2', 'Option 3', 'Option 4'];
  const orderingAlgorithmOptions = allPossibleOrderingAlgorithm.map((option) => ({
    value: option,
    label: option,
  }));

  const handleAlgorithmChange = (selectedOption) => {
    setSelectedOrderingAlgorithm(selectedOption.value);
    onOrderingAlgorithmChange(selectedOption.value);
  };

  return (
    <Form.Group>
      <Form.Label>Ordering Algorithm</Form.Label>
      <Select
        isSearchable={false}
        options={orderingAlgorithmOptions}
        value={orderingAlgorithmOptions.find((option) => option.value === selectedOrderingAlgorithm)}
        onChange={handleAlgorithmChange}
      />
    </Form.Group>
  );
};

export default OrderingAlgorithmSelect;
