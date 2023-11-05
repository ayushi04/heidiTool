import React, { useState, useEffect } from 'react';
import { Container, Button } from 'react-bootstrap';
import { useLocation } from 'react-router-dom';
import Select from 'react-select';
import { fetchColumns } from '../api';
import OrderingAlgorithmSelect from '../components/OrderingAlgorithmSelect';
import SelectedDimensions from '../components/SelectedDimensions';
import OrderingDimensions from '../components/OrderingDimensions';
import Legend from '../components/Legend';
import { getImage, getConsolidatedImage } from '../api';
import LoadingOverlay from '../components/LoadingOverlay';
import Tab from '../components/Tab';

const Heidi = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const datasetPath = searchParams.get('datasetPath');
  const [allPossibleDimensions, setAllPossibleDimensions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('consolidated');
  const [imageSrc, setImageSrc] = useState(null);
  const [consolidatedImageSrc, setConsolidatedImageSrc] = useState(null);
  const [selectedDimensions, setSelectedDimensions] = useState([]);
  const [selectedOrderingAlgorithm, setSelectedOrderingAlgorithm] = useState('');
  const [selectedOrderingDimensions, setSelectedOrderingDimensions] = useState([]);

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
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  const renderImage = () => (
    <img src={imageSrc} alt="Image" />
  );

  const renderConsolidatedImage = () => (
    <img src={consolidatedImageSrc} alt="Consolidated Image" />
  );

  const renderLoading = () => (
    <>
      <p>Loading...</p>
      <LoadingOverlay />
    </>
  );

  const renderContent = () => {
    if (loading) {
      return renderLoading();
    } else if (result && result.status === 'success') {
      return activeTab === 'image' ? renderImage() : renderConsolidatedImage();
    } else {
      return <p>No image available. Please select options and submit.</p>;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await getImage(datasetPath, selectedOrderingAlgorithm, selectedOrderingDimensions, selectedDimensions);
      setResult(result);

      if (result.status === 'success') {
        const imgData = result.consolidated_image.data;
        const contentType = result.consolidated_image.content_type;
        const dataUrl = `data:${contentType};base64,${imgData}`;
        setImageSrc(dataUrl);
      } else {
        console.error('Error fetching image for dataset:', datasetPath, 'with ordering algorithm:', selectedOrderingAlgorithm, 'and ordering dimensions:', selectedOrderingDimensions);
        console.error('Error:', result.error);
      }

      const consolidatedImageResult = await getConsolidatedImage(datasetPath, selectedOrderingAlgorithm, selectedDimensions);

      if (consolidatedImageResult.status === 'success') {
        const imgData = consolidatedImageResult.consolidated_image.data;
        const contentType = consolidatedImageResult.consolidated_image.content_type;
        const dataUrl = `data:${contentType};base64,${imgData}`;
        setConsolidatedImageSrc(dataUrl);
      } else {
        console.error('Error fetching consolidated image for dataset:', datasetPath, 'with ordering algorithm:', selectedOrderingAlgorithm, 'and ordering dimensions:', selectedOrderingDimensions);
        console.error('Error:', consolidatedImageResult.error);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container fluid>
      <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'stretch', height: '100%' }}>
        {/* Left Sidebar */}
        <div style={{ flex: '0 0 20%' }}>
          {/* Placeholder for the first column */}
        </div>

        {/* Ordering Options */}
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

      {/* Tab Component */}
      <div style={{ display: 'flex', flexDirection: 'row', marginTop: '50px' }}>
        <div style={{ flex: '0 0 20%' }}>
          {/* Placeholder for the first column */}
        </div>
        <Tab activeTab={activeTab} onTabChange={handleTabChange} />
      </div>

      {/* Main Content */}
      <div style={{ display: 'flex', flexDirection: 'row', marginTop: '50px' }}>
        {/* Selected Dimensions */}
        <div style={{ flex: '0 0 20%' }}>
          <SelectedDimensions allPossibleDimensions={allPossibleDimensions} onSelectedDimensionsChange={handleDimensionsChange} />
        </div>

        {/* Image/Consolidated Image */}
        <div style={{ flex: '0 0 60%' }}>
          <div style={{ flex: '1', marginRight: '10px' }}>
            {renderContent()}
          </div>
        </div>

        {/* Legend */}
        <div style={{ flex: '0 0 20%' }}>
          {loading ? null : result && result.status === 'success' ? (
            <p><Legend legendData={result.legend} /></p>
          ) : null}
        </div>
      </div>
    </Container>
  );
};

export default Heidi;
