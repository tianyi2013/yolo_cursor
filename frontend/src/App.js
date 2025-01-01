import React from 'react';
import { Box, Container, Typography, Paper, createTheme, ThemeProvider } from '@mui/material';
import ImageProcessor from './components/ImageProcessor';

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 3px 5px 2px rgba(0, 0, 0, .1)',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Box
        sx={{
          minHeight: '100vh',
          backgroundColor: '#f5f5f5',
          py: 4,
        }}
      >
        <Container maxWidth="lg">
          <Paper
            elevation={3}
            sx={{
              p: 4,
              mb: 4,
              background: 'linear-gradient(45deg, #1976d2 30%, #2196f3 90%)',
              color: 'white',
            }}
          >
            <Typography 
              variant="h3" 
              component="h1" 
              gutterBottom
              sx={{ 
                fontWeight: 'bold',
                textAlign: 'center',
                textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
              }}
            >
              YOLO Object Detection
            </Typography>
            <Typography 
              variant="h6" 
              component="h2"
              sx={{ 
                textAlign: 'center',
                opacity: 0.9,
              }}
            >
              Upload an image to detect objects using YOLO
            </Typography>
          </Paper>
          <ImageProcessor />
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App; 