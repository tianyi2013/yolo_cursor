import React, { useState } from 'react';
import {
  Box,
  Button,
  Paper,
  CircularProgress,
  Alert,
  Typography,
  Fade,
} from '@mui/material';
import { CloudUpload, Image, PictureAsPdf } from '@mui/icons-material';
import { processImage, getDownloadUrl } from '../services/api';
import ImageViewer from './ImageViewer';

const ImageProcessor = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [processedData, setProcessedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setPreview(URL.createObjectURL(file));
    setProcessedData(null);
    setError(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);

    try {
      const data = await processImage(selectedFile);
      setProcessedData(data);
    } catch (err) {
      setError('Error processing image. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (filename) => {
    if (!processedData) return;
    window.open(getDownloadUrl(processedData.request_id, filename), '_blank');
  };

  return (
    <Box sx={{ mb: 4 }}>
      <Paper 
        sx={{ 
          p: 3, 
          mb: 3,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 2,
          background: 'white',
        }}
      >
        <input
          accept="image/*"
          type="file"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
          id="image-input"
        />
        <label htmlFor="image-input">
          <Button
            variant="contained"
            component="span"
            startIcon={<Image />}
            sx={{
              px: 4,
              py: 1.5,
              borderRadius: 2,
              fontSize: '1.1rem',
            }}
          >
            Select Image
          </Button>
        </label>

        {selectedFile && (
          <Button
            variant="contained"
            onClick={handleUpload}
            disabled={loading}
            startIcon={<CloudUpload />}
            sx={{
              px: 4,
              py: 1.5,
              borderRadius: 2,
              fontSize: '1.1rem',
              backgroundColor: '#4caf50',
              '&:hover': {
                backgroundColor: '#388e3c',
              },
            }}
          >
            Process Image
          </Button>
        )}

        {selectedFile && (
          <Typography variant="body1" color="text.secondary">
            Selected: {selectedFile.name}
          </Typography>
        )}
      </Paper>

      {error && (
        <Fade in={true}>
          <Alert 
            severity="error" 
            sx={{ 
              mb: 3,
              borderRadius: 2,
            }}
          >
            {error}
          </Alert>
        </Fade>
      )}

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
          <CircularProgress size={60} />
        </Box>
      )}

      <Box 
        sx={{ 
          display: 'flex', 
          gap: 3,
          flexDirection: { xs: 'column', md: 'row' }
        }}
      >
        {preview && (
          <Fade in={true}>
            <Box sx={{ flex: 1 }}>
              <ImageViewer title="Original Image" imageSrc={preview} />
            </Box>
          </Fade>
        )}

        {processedData && (
          <Fade in={true}>
            <Box sx={{ flex: 1 }}>
              <Paper sx={{ p: 3, height: '100%', display: 'flex', flexDirection: 'column' }}>
                <Typography variant="h6" gutterBottom>
                  Processed Image
                </Typography>
                <Box sx={{ flex: 1, mb: 2 }}>
                  <img
                    src={getDownloadUrl(
                      processedData.request_id,
                      processedData.annotated_filename
                    )}
                    alt="Processed"
                    style={{ 
                      width: '100%',
                      height: 'auto',
                      borderRadius: 8,
                      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                    }}
                  />
                </Box>
                <Button
                  variant="contained"
                  onClick={() => handleDownload(processedData.pdf_filename)}
                  startIcon={<PictureAsPdf />}
                  sx={{
                    mt: 'auto',
                    borderRadius: 2,
                    backgroundColor: '#f44336',
                    '&:hover': {
                      backgroundColor: '#d32f2f',
                    },
                  }}
                >
                  Download PDF Report
                </Button>
              </Paper>
            </Box>
          </Fade>
        )}
      </Box>
    </Box>
  );
};

export default ImageProcessor; 