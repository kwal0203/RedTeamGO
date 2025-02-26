import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Textarea,
  VStack,
  useToast,
  Text,
  Card,
  CardBody,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
} from '@chakra-ui/react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

interface RealtimeResponse {
  result: string;
}

export default function RealtimeAnalysis() {
  const toast = useToast();
  const [prompt, setPrompt] = useState('');

  const toxicityMutation = useMutation({
    mutationFn: async (prompt: string) => {
      const response = await axios.post<RealtimeResponse>('http://localhost:8000/toxicity-detection-realtime', { prompt });
      return response.data;
    },
    onSuccess: () => {
      toast({
        title: 'Analysis Complete',
        description: 'Toxicity analysis has been completed successfully.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: 'Failed to complete toxicity analysis.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  const biasMutation = useMutation({
    mutationFn: async (prompt: string) => {
      const response = await axios.post<RealtimeResponse>('http://localhost:8000/bias-detection-realtime', { prompt });
      return response.data;
    },
    onSuccess: () => {
      toast({
        title: 'Analysis Complete',
        description: 'Bias analysis has been completed successfully.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: 'Failed to complete bias analysis.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    },
  });

  const handleToxicityAnalysis = () => {
    if (prompt.trim()) {
      toxicityMutation.mutate(prompt);
    }
  };

  const handleBiasAnalysis = () => {
    if (prompt.trim()) {
      biasMutation.mutate(prompt);
    }
  };

  return (
    <Box maxW="7xl" mx="auto" pt={5} px={{ base: 2, sm: 12, md: 17 }}>
      <Text fontSize="2xl" fontWeight="bold" mb={8}>
        Real-time Analysis
      </Text>

      <Card mb={8}>
        <CardBody>
          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel>Enter Prompt</FormLabel>
              <Textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Enter your prompt here..."
                size="lg"
                rows={5}
              />
            </FormControl>

            <Box>
              <Button
                colorScheme="blue"
                mr={4}
                onClick={handleToxicityAnalysis}
                isLoading={toxicityMutation.isPending}
              >
                Run Toxicity Analysis
              </Button>
              <Button
                colorScheme="purple"
                onClick={handleBiasAnalysis}
                isLoading={biasMutation.isPending}
              >
                Run Bias Analysis
              </Button>
            </Box>
          </VStack>
        </CardBody>
      </Card>

      <Tabs>
        <TabList>
          <Tab>Toxicity Results</Tab>
          <Tab>Bias Results</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            {toxicityMutation.data && (
              <Card>
                <CardBody>
                  <Text fontSize="xl" fontWeight="semibold" mb={4}>
                    Toxicity Analysis Results
                  </Text>
                  <pre style={{ whiteSpace: 'pre-wrap' }}>
                    {JSON.stringify(toxicityMutation.data, null, 2)}
                  </pre>
                </CardBody>
              </Card>
            )}
          </TabPanel>
          <TabPanel>
            {biasMutation.data && (
              <Card>
                <CardBody>
                  <Text fontSize="xl" fontWeight="semibold" mb={4}>
                    Bias Analysis Results
                  </Text>
                  <pre style={{ whiteSpace: 'pre-wrap' }}>
                    {JSON.stringify(biasMutation.data, null, 2)}
                  </pre>
                </CardBody>
              </Card>
            )}
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
}