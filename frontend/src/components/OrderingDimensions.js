import React, { useState } from 'react';
import Select from 'react-select';
import { Form } from 'react-bootstrap';

const OrderingDimensions = ({ allPossibleDimensions, onOrderingDimensionsChange }) => {
    const [selectedOrderingDimensions, setSelectedOrderingDimensions] = useState([]);

    const handleChange = (selectedOption) => {
        const updatedSelection = selectedOption.map((option) => option.value);
        setSelectedOrderingDimensions(updatedSelection);
        onOrderingDimensionsChange(updatedSelection);
    };

    return (
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
            onChange={handleChange}
        />
    </Form.Group>
    );
};

export default OrderingDimensions;
