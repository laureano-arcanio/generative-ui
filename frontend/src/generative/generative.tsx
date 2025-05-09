import { useEffect, useState, useRef, useCallback, useMemo, useContext } from 'react';
import { LiveProvider, LiveError, LivePreview, LiveContext } from 'react-live';
import { useParams, Link } from 'react-router-dom';
import { personas, designers } from '../App';
import * as MUI from '@mui/material';
import  * as ICONS from '@mui/icons-material'
import { Box, Button, CircularProgress, Typography } from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import HomeIcon from '@mui/icons-material/Home';

interface GenerativeDetails {
  userPrefferences: string;
  rawComponent?: string;
  generatedPrompt?: string;
}


function App() {
  // Updated to support both persona and designer IDs
  const { personaId, designerId } = useParams<{ personaId: string, designerId: string }>();
  
  const [data, setData] = useState<GenerativeDetails | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const requestMadeRef = useRef<boolean>(false);
  const effectRunRef = useRef(false);
  const [livePreviewError, setLivePreviewError] = useState<string | null>(null);
  const retryCountRef = useRef(0); // Track retry attempts
  const [showPrompt, setShowPrompt] = useState(false); // State to toggle prompt visibility

  const LiveErrorCustom = (props) => {
    const { error } = useContext(LiveContext);

    // Retry up to 3 times before showing the error
    useEffect(() => {
      if (error) {
        console.error(`LivePreview error detected (attempt ${retryCountRef.current + 1}/3):`, error);

        if (retryCountRef.current < 2) { // Retry up to 3 times (0, 1, 2)
          retryCountRef.current += 1;

          const timer = setTimeout(() => {
            handleRegenerate(false); // Retry without resetting retry count
          }, 2000); // Retry after 2 seconds

          return () => clearTimeout(timer);
        } else {
          // After 3 attempts, show the error
          handleLiveError(error.toString());
          retryCountRef.current = 0; // Reset retry count for next cycle
        }
      }
    }, [error]);

    // Only show error after 3 failed attempts
    return (retryCountRef.current >= 2 && error) ? <span {...props}>{error}</span> : null;
  };

  const handleSubmit = useCallback(async () => {
    console.log("handleSubmit called with personaId:", personaId, "designerId:", designerId);
    
    if (!personaId || !designerId) {  
      console.log("Skipping request - missing IDs");
      return;
    }
    
    // Reset the flag to allow regeneration
    requestMadeRef.current = true;
    
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/generative/react', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          personaId: parseInt(personaId, 10),
          designerId: parseInt(designerId, 10)
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to submit data');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  }, [personaId, designerId]);

  // Handle LivePreview errors
  const handleLiveError = useCallback((errorMessage: string) => {
    console.error(`LivePreview error (after ${retryCountRef.current + 1} attempts):`, errorMessage);
    if (retryCountRef.current >= 2) {
      setLivePreviewError(errorMessage); // Show error after retries
    }
  }, []);

  // Reset error state when regenerating
  const handleRegenerate = useCallback((resetRetryCount = true) => {
    requestMadeRef.current = false;
    setLivePreviewError("We are regenerating your component...");

    if (resetRetryCount) {
      retryCountRef.current = 0; // Reset retry count for manual regeneration
    }

    handleSubmit();
  }, [handleSubmit]);

  useEffect(() => {
    // React 18 StrictMode runs effects twice in development
    // Use this pattern to ensure we only make one API call
    if (personaId && designerId && !effectRunRef.current) {
      effectRunRef.current = true;
      console.log("Calling handleSubmit"); 
      handleSubmit();
    }
    
    return () => {
      // Only reset on unmount, not between re-renders
      if (!personaId || !designerId) {
        effectRunRef.current = false;
        requestMadeRef.current = false;
      }
    };
  }, [personaId, designerId, handleSubmit]);

  const selectedPersona = useMemo(() => {
    if (!personaId) return null;
    const id = parseInt(personaId, 10);
    return personas.find((persona) => persona.id === id) || null;
  }, [personaId]);
  
  const selectedDesigner = useMemo(() => {
    if (!designerId) return null;
    const id = parseInt(designerId, 10);
    return designers.find((designer) => designer.id === id) || null;
  }, [designerId]);

  /**
   * Parses a raw component string into valid React code for react-live
   * @param rawCode - The raw component code as a string
   * @returns Properly formatted code for react-live to render
   */
  const parseComponentCode = (rawCode: string): string => {
    let code = rawCode.replace("\\", '');
    return code.trim();
  };

  // Create a context object with all the MUI components we want to make available
  const scope = useMemo(() => {
    return {
      // MUI components
      MUI,
      // React hooks
      useState,
      useEffect,
      useRef,
      ICONS ,
    };
  }, []);

  // Use the parsing function with the raw data
  const parsedComponent = data?.rawComponent ? parseComponentCode(data.rawComponent) : '';
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 relative">
      {/* Position buttons at top left */}
      <Box sx={{ 
        position: 'absolute',
        top: 20,
        left: 20,
        display: 'flex',
        gap: 2,
      }}>
        <Button
          onClick={handleRegenerate}
          variant="contained"
          color="primary"
          startIcon={<RefreshIcon sx={{marginLeft: 2}}/>}
          sx={{
            fontSize: '1.1rem',
            py: 1.2,
            px: 0,
            borderRadius: '8px',
            bgcolor: '#ff6d00', 
            '&:hover': {
              bgcolor: '#e65100',
            },
            boxShadow: '0 4px 12px rgba(255, 109, 0, 0.3)',
            animation: 'pulse 2s infinite',
            '@keyframes pulse': {
              '0%': { boxShadow: '0 4px 12px rgba(255, 109, 0, 0.3)' },
              '50%': { boxShadow: '0 4px 20px rgba(255, 109, 0, 0.5)' },
              '100%': { boxShadow: '0 4px 12px rgba(255, 109, 0, 0.3)' }
            }
          }}
        >
          &nbsp;
        </Button>

        <Button
          component={Link}
          to="/"
          variant="outlined"
          sx={{
            fontSize: '1.1rem',
            py: 1.2,
            px: 2,
            borderRadius: '8px',
            borderColor: '#2196f3',
            color: '#2196f3',
            '&:hover': {
              bgcolor: 'rgba(33, 150, 243, 0.08)',
              borderColor: '#1976d2',
            }
          }}
        >
          <HomeIcon />
        </Button>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
          <CircularProgress />
          <Typography variant="body1" color="text.secondary" sx={{ fontSize: '1.2rem' }}>
            Crafting your experience...
          </Typography>
        </Box>
      ) : parsedComponent ? (
        <div className="mb-6">
          {/* Display selected persona and designer information */}
          {selectedPersona && selectedDesigner && !livePreviewError && (
            <Box sx={{ 
              display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center', 
              mb: 4, 
              p: 1, 

              maxWidth: '800px'
            }}>

              <Box sx={{ display: 'flex', width: '100%' }}>
                <Box sx={{ flex: 1}}>
                  <Typography variant="body2" sx={{ mt: 1,  }}>
                    Persona: {selectedPersona.persona}
                  </Typography>
                </Box>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="body2" sx={{ mt: 1, }}>
                    Style: {selectedDesigner.persona}
                  </Typography>
                </Box>
              </Box>
            </Box>
          )}
          
          <LiveProvider code={parsedComponent} scope={scope}>
            <div className="overflow-hidden">
              <div className="" style={{ minWidth: '500px' }}>
                <LivePreview />
              </div>
              <LiveErrorCustom 
                className="text-red-500 p-2 text-sm" 
                onError={(error) => handleLiveError(error.toString())}
              />
            </div>
          </LiveProvider>
          
          {livePreviewError && (
            <Box sx={{ 
              // display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center', 
              gap: 2,
              mt: 3,
              p: 3,
              bgcolor: 'warnig.light',
              borderRadius: 2,
              display: 'none'
            }}>
              <Typography variant="body1">
                One moment, please...
              </Typography>
              <Button
                onClick={() => handleRegenerate(true)}
                variant="contained"
                color="error"
                startIcon={<RefreshIcon />}
                sx={{ mt: 1 }}
              >
                Generate
              </Button>
            </Box>
          )}
          
          {/* Don't like it button with refresh icon */}
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'center', 
            gap: 2,
            mt: 4,
            mb: 2
          }}>
          </Box>

          <Box sx={{ mt: 4, textAlign: 'center', display: livePreviewError ? 'none' : 'block' }}>
            <Button
              variant="outlined"
              onClick={() => setShowPrompt(!showPrompt)}
              sx={{
                fontSize: '1rem',
                py: 1,
                px: 3,
                borderRadius: '8px',
                borderColor: '#1976d2',
                color: '#1976d2',
                '&:hover': {
                  bgcolor: 'rgba(25, 118, 210, 0.08)',
                  borderColor: '#1565c0',
                },
              }}
            >
              {showPrompt ? 'Hide Prompt' : 'Show Prompt'}
            </Button>
            {showPrompt && data?.generatedPrompt && (
              <Box
                sx={{
                  mt: 2,
                  p: 2,
                  bgcolor: 'background.paper',
                  borderRadius: 2,
                  boxShadow: 1,
                  maxWidth: '800px',
                  textAlign: 'left',
                  whiteSpace: 'pre-wrap',
                  wordBreak: 'break-word',
                }}
              >
                <Typography variant="body2" color="text.secondary">
                  {data.generatedPrompt}
                </Typography>
              </Box>
            )}
          </Box>
        </div>
      ) : error ? (
        <Box sx={{ color: 'error.main', p: 2, bgcolor: 'success.light', borderRadius: 1 }}>
          <Typography variant="body1">
            Working, one moment: {error}
          </Typography>
        </Box>
      ) : null}
      
    </div>
  )
}

export default App
