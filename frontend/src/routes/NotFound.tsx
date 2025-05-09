import { useRouteError } from 'react-router-dom';
import { Typography, Button, Box, Container } from '@mui/material';
import { Link } from 'react-router-dom';

export default function NotFound() {
  const error = useRouteError();
  
  return (
    <Container maxWidth="sm">
      <Box className="flex flex-col items-center justify-center min-h-screen text-center">
        <Typography variant="h2" component="h1" gutterBottom>
          404
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Page Not Found
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
          {error?.statusText || error?.message || 
           "The page you're looking for doesn't exist or has been moved."}
        </Typography>
        <Button 
          component={Link}
          to="/"
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
        >
          Go to Home
        </Button>
      </Box>
    </Container>
  );
}