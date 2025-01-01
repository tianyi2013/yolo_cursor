import React from 'react';
import { Paper, Typography, Box } from '@mui/material';

const ImageViewer = ({ title, imageSrc }) => {
  return (
    <Paper 
      sx={{ 
        p: 3,
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <Box sx={{ flex: 1 }}>
        <img
          src={imageSrc}
          alt={title}
          style={{ 
            width: '100%',
            height: 'auto',
            borderRadius: 8,
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          }}
        />
      </Box>
    </Paper>
  );
};

export default ImageViewer; 