import React, { useState, useEffect } from 'react';
import { fetchColumns } from '../api'; 
import { useLocation } from 'react-router-dom';

function ColumnsDisplay() {
  const [columns, setColumns] = useState([]);
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const datasetPath = searchParams.get('datasetPath');
  

  useEffect(() => {
    // Fetch the list of columns from getColumns API here
    // You can use the Fetch API or Axios to make a GET request to your API endpoint
    const loadColumns = async () => {
        try {
          const fetchedColumns = await fetchColumns(datasetPath);
          setColumns(fetchedColumns.columns);
        } catch (error) {
          console.error('Error fetching columns:', error.message);
        }
      };
      loadColumns();
  }, []);

  return (
    
    <div className="container">
      <h2>Columns in the Dataset</h2>
      <ul>
        {columns && columns.map((column, index) => (
          <li key={index}>{column}</li>
        ))}
      </ul>
    </div>
  );
}

export default ColumnsDisplay;
