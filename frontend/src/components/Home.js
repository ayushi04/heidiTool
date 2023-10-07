import React, { useState } from 'react';
import { uploadFile } from '../api'; // Import the API function


function Home() {
  const [file, setFile] = useState(null);
  const [fixMethod, setFixMethod] = useState('skip');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFixMethodChange = (e) => {
    setFixMethod(e.target.value);
  };

  
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (file) {
        const result = await uploadFile(file, fixMethod);
        // Handle the API response, e.g., display a success message
        console.log('Upload success:', result);
      } else {
        // Handle case where no file is selected
        console.error('No file selected');
      }
    } catch (error) {
      // Handle API request errors, e.g., display an error message
      console.error('Upload error:', error);
    }
  };

  return (
    <div className="container">
      {/* Assuming you have imported Bootstrap CSS */}
      
      <div className="row">
        <div className="col-md-4 col-sm-12">
          <div className="card" style={{ width: '20rem' }}>
            <div className="card-block">
              <h4 className="card-title text-center text-warning">CSV</h4>
              <p className="card-text text-center">Upload your .csv file here and get it cleaned</p>
              <form onSubmit={handleSubmit} encType="multipart/form-data">
                <div className="form-group">
                  <input name="file" type="file" className="form-control-file" id="exampleInputFile" aria-describedby="fileHelp" onChange={handleFileChange} />
                  <small id="fileHelp" className="form-text text-muted">Upload your file here and click on the upload button</small>
                </div>
                <div className="form-group">
                  <label htmlFor="fix-missing">How to fix missing values?</label>
                  <select className="form-control" id="fix-missing" name="fix" onChange={handleFixMethodChange}>
                    <option value="skip">Skip tuple/row</option>
                    <option value="mean">Replace by mean</option>
                    <option value="median">Replace by median</option>
                    <option value="max frequent">Replace by maximum frequent value</option>
                    <option value="max">Replace by maximum value</option>
                    <option value="min">Replace by minimum value</option>
                  </select>
                </div>
                <div className="text-center">
                  <button type="submit" className="btn btn-warning">Upload CSV</button>
                </div>
              </form>
            </div>
          </div>
        </div>
        <div className="col-md-4 col-sm-12">
          <div className="card" style={{ width: '20rem' }}>
            <div className="card-block">
              <h4 className="card-title text-center text-success">JSON</h4>
              <p className="card-text text-center">Upload your .json file here and get it cleaned</p>
              <form action="http://localhost:8080/upload" method="POST" encType="multipart/form-data">
                <div className="form-group">
                  <input name="file" type="file" className="form-control-file" id="exampleInputFile" aria-describedby="fileHelp" onChange={handleFileChange} />
                  <small id="fileHelp" className="form-text text-muted">Upload your file here and click on the upload button</small>
                </div>
                <div className="form-group">
                  <label htmlFor="fix-missing">How to fix missing values?</label>
                  <select className="form-control" id="fix-missing" name="fix" onChange={handleFixMethodChange}>
                    <option value="skip">Skip tuple/row</option>
                    <option value="mean">Replace by mean</option>
                    <option value="median">Replace by median</option>
                    <option value="max frequent">Replace by maximum frequent value</option>
                    <option value="max">Replace by maximum value</option>
                    <option value="min">Replace by minimum value</option>
                  </select>
                </div>
                <div className="text-center">
                  <button type="submit" className="btn btn-success">Upload JSON</button>
                </div>
              </form>
            </div>
          </div>
        </div>
        <div className="col-md-4 col-sm-12">
          <div className="card" style={{ width: '20rem' }}>
            <div className="card-block">
              <h4 className="card-title text-center text-info">TSV</h4>
              <p className="card-text text-center">Upload your .tsv file here and get it cleaned</p>
              <form action="http://localhost:8080/upload" method="POST" encType="multipart/form-data">
                <div className="form-group">
                  <input name="file" type="file" className="form-control-file" id="exampleInputFile" aria-describedby="fileHelp" onChange={handleFileChange} />
                  <small id="fileHelp" className="form-text text-muted">Upload your file here and click on the upload button</small>
                </div>
                <div className="form-group">
                  <label htmlFor="fix-missing">How to fix missing values?</label>
                  <select className="form-control" id="fix-missing" name="fix" onChange={handleFixMethodChange}>
                    <option value="skip">Skip tuple/row</option>
                    <option value="mean">Replace by mean</option>
                    <option value="median">Replace by median</option>
                    <option value="max frequent">Replace by maximum frequent value</option>
                    <option value="max">Replace by maximum value</option>
                    <option value="min">Replace by minimum value</option>
                  </select>
                </div>
                <div className="text-center">
                  <button type="submit" className="btn btn-info">Upload TSV</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;