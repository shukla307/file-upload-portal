import React from 'react';

const FileList = ({ files, onDelete }) => {
  return (
    <ul>
      {files.map((file) => (
        <li key={file.name}>
          <span>{file.name}</span>
          <button onClick={() => onDelete(file.name)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

export default FileList;