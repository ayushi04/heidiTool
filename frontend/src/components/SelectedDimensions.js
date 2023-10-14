import React, { useState } from 'react';
import { Form } from 'react-bootstrap';

const SelectedDimensions = ({ allPossibleDimensions, onSelectedDimensionsChange }) => {
  const [selectedDimensions, setSelectedDimensions] = useState([]);

  const handleCheckboxChange = (event) => {
    const { name, checked } = event.target;
    const updatedSelection = { ...selectedDimensions, [name]: checked }
    setSelectedDimensions(updatedSelection);
    const selectedDims = Object.keys(updatedSelection).filter((dim) => updatedSelection[dim]);
    onSelectedDimensionsChange(selectedDims);
  };

  return (
    <div>
      <h4>Dimensions</h4>
      <Form>
        {/* Render the checkboxes here */}
        {allPossibleDimensions.map((dimension) => (
          <div key={dimension}>
            <label>
              <input
                type="checkbox"
                name={dimension}
                // checked={selectedDimensions.includes(dimension)}
                checked={selectedDimensions[dimension]}
                onChange={handleCheckboxChange}
              />
              {dimension}
            </label>
          </div>
        ))}
      </Form>
    </div>
  );
};

export default SelectedDimensions;
