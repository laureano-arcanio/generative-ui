import React, { useState, useEffect } from 'react';
import { 
  Chip, 
  Typography, 
  Paper, 
  Box, 
  Container,
  Stack,
  Button,
  Divider
} from '@mui/material';
import { Link } from 'react-router-dom';

import './App.css';


export interface Persona {
  id: number;
  prompt: string;
  persona: string;
  colors?: string[];
}

// Adding a new Designer interface to match backend structure
export interface Designer {
  id: number;
  prompt: string;
  name?: string;
  persona?: string;
}

// New designers array that matches the backend self.designers structure
export const designers: Designer[] = [
  {
    id: 1,
    prompt: `
      I prefer a clean, modern, minimalist design with plenty of white space and subtle typography. 
      Content should be direct, uncluttered, and avoid unnecessary visual embellishments. 
      Keep the structure simple and focus on clarity and hierarchy of information. 
      Action buttons should be bold and high-contrast, but minimal in decoration. 
      The toggle switch should be sleek and unobtrusive. Icons are optional and should be line-based if included.`,
      persona: "Minimalist Designer",
  },
  {
    id: 2,
    prompt: `
      I want a fun, colorful, and lively UI with rounded corners, soft shadows, and vibrant accent colors for each plan. 
      Use illustrative icons or small playful graphics alongside feature lists to enhance approachability. 
      Typography can be a bit more expressive and casual while staying readable. 
      The toggle switch should have a fun animation when switching between “Monthly” and “Yearly.” Action buttons should be big, colorful, and inviting.`,
    persona: "Playful & Creative Designer",
  },
  {
    id: 3,
    prompt: `
      I prefer a formal, polished, enterprise-level design with structured grid layouts, 
      sharp lines, and a professional color palette (e.g., gray, white, with occasional accent colors).
      Icons should be minimal but professional, aligning with business software aesthetics.
      Use clear typography with consistent weights to convey trust and authority. 
      The toggle should feel part of a control panel, and action buttons should be subtle but clear, prioritizing function over flair.`,
    persona: "Professional & Corporate Designer",
  },
];

// Updated to match target_audiences in the Python file
export const personas: Persona[] = [
  {
    id: 1,
    prompt: "Event organizers looking to create a user-friendly form for event registration.",
    persona: "Event Organizer",
  },
  {
    id: 2,
    prompt: "Personal coaches building introspective intake forms for their clients.",
    persona: "Personal Coach",
  },
  {
    id: 3,
    prompt: "HR managers creating onboarding and employee insight forms with complex level of details.",
    persona: "HR Manager",
  },
]

function App() {
  const [selectedPersona, setSelectedPersona] = useState<Persona | null>(null);
  const [selectedDesigner, setSelectedDesigner] = useState<Designer | null>(null);

  useEffect(() => {
    if (personas.length > 0) {
      setSelectedPersona(personas[0]);
    }
    
    if (designers.length > 0) {
      setSelectedDesigner(designers[0]);
    }
  }, []);

  return (
    <Container maxWidth="md">
      <Box className="flex flex-col items-center justify-center min-h-screen p-6">
        <Typography 
          variant="h4" 
          gutterBottom
          sx={{ 
            fontFamily: '"Poppins", "Roboto", sans-serif',
            fontWeight: 600,
            color: '#424242',
            letterSpacing: '0.2px',
            mb: 5,
            position: 'relative',
            '&::after': {
              content: '""',
              position: 'absolute',
              width: '40%',
              height: '3px',
              background: 'linear-gradient(90deg, #3f51b5, #2196f3)',
              bottom: '-8px',
              left: '30%',
              borderRadius: '2px'
            }
          }}
        >
          Hey there! Choose your preferences
        </Typography>
        
        <Typography 
          variant="h6" 
          gutterBottom
          sx={{ 
            fontFamily: '"Poppins", "Roboto", sans-serif',
            color: '#424242',
            mt: 2,
            mb: 2
          }}
        >
          1. Select your target audience
        </Typography>
        
        <Stack direction="row" spacing={2} sx={{ mb: 4, flexWrap: 'wrap', justifyContent: 'center' }}>
          {personas.map((persona) => (
            <Chip
              key={persona.id}
              label={persona.persona}
              onClick={() => setSelectedPersona(persona)}
              color={selectedPersona?.id === persona.id ? "primary" : "default"}
              variant={selectedPersona?.id === persona.id ? "filled" : "outlined"}
              sx={{ 
                my: 2,
                marginBottom: "20px !important",
                fontSize: '0.9rem',
                px: 2,
                py: 1,
                height: 'auto',
                '& .MuiChip-label': {
                  padding: '8px 4px',
                }
              }}
            />
          ))}
        </Stack>
        
        {selectedPersona && (
          <Paper elevation={2} sx={{ p: 3, bgcolor: '#f8f9fa', borderLeft: '4px solid #1976d2', mb: 5, width: '100%' }}>
            <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
              "{selectedPersona.prompt}"
            </Typography>
          </Paper>
        )}
        
        <Divider sx={{ width: '80%', my: 3 }} />
        
        <Typography 
          variant="h6" 
          gutterBottom
          sx={{ 
            fontFamily: '"Poppins", "Roboto", sans-serif',
            color: '#424242',
            mt: 2,
            mb: 2
          }}
        >
          2. Choose your design style
        </Typography>
        
        <Stack direction="row" spacing={2} sx={{ mb: 4, flexWrap: 'wrap', justifyContent: 'center' }}>
          {designers.map((designer) => (
            <Chip
              key={designer.id}
              label={designer.persona || "Style " + designer.id}
              onClick={() => setSelectedDesigner(designer)}
              color={selectedDesigner?.id === designer.id ? "secondary" : "default"}
              variant={selectedDesigner?.id === designer.id ? "filled" : "outlined"}
              sx={{ 
                my: 2,
                marginBottom: "20px !important",
                fontSize: '0.9rem',
                px: 2,
                py: 1,
                height: 'auto',
                '& .MuiChip-label': {
                  padding: '8px 4px',
                }
              }}
            />
          ))}
        </Stack>
        
        {selectedDesigner && (
          <Paper elevation={2} sx={{ p: 3, bgcolor: '#f8f9fa', borderLeft: '4px solid #9c27b0', mb: 5, width: '100%' }}>
            <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
              "{selectedDesigner.prompt}"
            </Typography>
          </Paper>
        )}
        
        {selectedPersona && selectedDesigner && (
          <Button
            component={Link}
            to={`/generated-ui/${selectedDesigner.id}/${selectedPersona.id}`}
            variant="contained"
            size="large"
            sx={{
              bgcolor: '#2e7d32',
              '&:hover': {
                bgcolor: '#1b5e20',
              },
              py: 1.5,
              px: 4,
              fontSize: '1.1rem',
              fontWeight: 'bold',
              borderRadius: '8px',
              boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
              textTransform: 'none',
              mt: 4
            }}
          >
            Start Crafting
          </Button>
        )}
      </Box>
    </Container>
  )
}

export default App
