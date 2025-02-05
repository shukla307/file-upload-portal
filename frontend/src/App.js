import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileUpload from './components/FileUpload';
import FileList from './components/FileList';
import './styles.css';

function App() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    const response = await axios.get('http://localhost:5000/api/files');
    setFiles(response.data);
  };

  const handleDelete = async (filename) => {
    await axios.delete(`http://localhost:5000/api/files/${filename}`);
    fetchFiles();
  };

  return (
    <div className="App">
      <h1>File Upload Portal</h1>
      <FileUpload onUpload={fetchFiles} />
      <FileList files={files} onDelete={handleDelete} />
    </div>
  );
}

export default App;