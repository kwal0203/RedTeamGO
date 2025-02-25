import React from 'react';
import { ChakraProvider, Box } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

// Pages
import Dashboard from './pages/Dashboard';
import ToxicityBatch from './pages/ToxicityBatch';
import BiasBatch from './pages/BiasBatch';
import RealtimeAnalysis from './pages/RealtimeAnalysis';

// Theme
import theme from './theme';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider theme={theme}>
        <Router>
          <Box minH="100vh" bg="gray.50">
            <Navbar />
            <Box display="flex">
              <Sidebar />
              <Box flex="1" p={8}>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/toxicity-batch" element={<ToxicityBatch />} />
                  <Route path="/bias-batch" element={<BiasBatch />} />
                  <Route path="/realtime" element={<RealtimeAnalysis />} />
                </Routes>
              </Box>
            </Box>
          </Box>
        </Router>
      </ChakraProvider>
    </QueryClientProvider>
  );
}

export default App;