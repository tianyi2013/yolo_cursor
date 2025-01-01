import React, { useRef, useState, useEffect } from 'react';
import {
  Box,
  Button,
  Paper,
  Typography,
  CircularProgress,
} from '@mui/material';
import { Videocam, VideocamOff } from '@mui/icons-material';
import axios from 'axios';

const CameraView = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [hasCamera, setHasCamera] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [loading, setLoading] = useState(true);
  const processingRef = useRef(false);

  useEffect(() => {
    // Check if camera is available
    navigator.mediaDevices.enumerateDevices()
      .then(devices => {
        const videoDevices = devices.filter(device => device.kind === 'videoinput');
        setHasCamera(videoDevices.length > 0);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error checking camera:", err);
        setHasCamera(false);
        setLoading(false);
      });

    return () => {
      stopCamera();
    };
  }, []);

  const processFrame = async (canvas) => {
    if (!processingRef.current) return;

    try {
      // Draw the current video frame to canvas first
      const video = videoRef.current;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Add moderate delay to ensure stable processing
      await new Promise(resolve => setTimeout(resolve, 200));

      // Convert canvas to blob
      const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.8));
      const formData = new FormData();
      formData.append('file', blob, 'frame.jpg');

      // Send to backend
      const response = await axios.post('http://localhost:8000/process-frame/', formData, {
        responseType: 'blob',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 10000  // 10 second timeout
      });

      // Display processed frame
      const imageUrl = URL.createObjectURL(response.data);
      const img = new Image();
      img.onload = () => {
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(imageUrl);
        
        // Process next frame
        if (processingRef.current) {
          // Add delay between frames for more stable processing
          setTimeout(() => processFrame(canvas), 200);
        }
      };
      img.src = imageUrl;

    } catch (error) {
      console.error('Error processing frame:', error);
      if (processingRef.current) {
        setTimeout(() => processFrame(canvas), 1000);  // Longer delay on error to recover
      }
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 },
          frameRate: { ideal: 10 },  // Further reduce framerate for stability
          height: { ideal: 480 }
        } 
      });
      
      if (videoRef.current && canvasRef.current) {
        videoRef.current.srcObject = stream;
        const canvas = canvasRef.current;
        const video = videoRef.current;
        
        // Wait for video metadata to load
        video.onloadedmetadata = () => {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
        };
        
        video.onplay = () => {
          setIsStreaming(true);
          processingRef.current = true;
          setIsProcessing(true);
          processFrame(canvas);
        };
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      setIsStreaming(false);
    }
  };

  const stopCamera = () => {
    processingRef.current = false;
    setIsProcessing(false);
    
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsStreaming(false);
    }

    // Clear canvas
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  };

  const toggleCamera = () => {
    if (isStreaming) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Paper 
      sx={{ 
        p: 3,
        mb: 3,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 2
      }}
    >
      <Typography variant="h6" gutterBottom>
        Camera View
      </Typography>

      <Button
        variant="contained"
        onClick={toggleCamera}
        disabled={!hasCamera}
        startIcon={isStreaming ? <VideocamOff /> : <Videocam />}
        sx={{
          px: 4,
          py: 1.5,
          borderRadius: 2,
          fontSize: '1.1rem',
          backgroundColor: isStreaming ? '#f44336' : '#4caf50',
          '&:hover': {
            backgroundColor: isStreaming ? '#d32f2f' : '#388e3c',
          },
        }}
      >
        {isStreaming ? 'Stop Camera' : 'Start Camera'}
      </Button>

      {!hasCamera && (
        <Typography color="error">
          No camera detected
        </Typography>
      )}

      <Box
        sx={{
          width: '100%',
          maxWidth: '800px',
          position: 'relative',
          display: isStreaming ? 'block' : 'none',
        }}
      >
        <video
          ref={videoRef}
          autoPlay
          playsInline
          style={{ display: 'none' }}
        />
        <canvas
          ref={canvasRef}
          style={{
            width: '100%',
            height: 'auto',
            borderRadius: 8,
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          }}
        />
        {isProcessing && (
          <Box
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              backgroundColor: 'rgba(0,0,0,0.5)',
              color: 'white',
              padding: '4px 8px',
              borderRadius: 4,
              fontSize: '0.8rem',
            }}
          >
            Processing...
          </Box>
        )}
      </Box>
    </Paper>
  );
};

export default CameraView; 