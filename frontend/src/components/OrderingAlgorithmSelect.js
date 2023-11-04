import React, { useState } from 'react';
import Select from 'react-select';
import { Form } from 'react-bootstrap';

const OrderingAlgorithmSelect = ({ onOrderingAlgorithmChange }) => {
  const [selectedOrderingAlgorithm, setSelectedOrderingAlgorithm] = useState('');

  // Ordering algorithm options
  const allPossibleOrderingAlgorithm = ['centroid_distance', 'knn_bfs', 'connected_distance', 'mst_distance', 'pca_ordering', 'tsne_ordering', 'dimension', 'nearest_to_all', 'euclidian_distance'];
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
