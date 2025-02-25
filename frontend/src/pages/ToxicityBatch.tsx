import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  NumberInput,
  NumberInputField,
  Switch,
  VStack,
  useToast,
  Text,
  Textarea,
  Card,
  CardBody,
} from '@chakra-ui/react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

interface ToxicityBatchRequest {
  model: {
    name: string;
    description: string;
    base_url: string | null;
  };
  num_samples: number;
  random: boolean;
  database_prompts: boolean;
  user_prompts: string[] | null;
  user_topics: string[] | null;
}

export default function ToxicityBatch() {
  const toast = useToast();
  const [formData, setFormData] = useState<ToxicityBatchRequest>({
    model: {
      name: 'openai',
      description: 'OpenAI model for toxicity testing',
      base_url: null,
    },
    num_samples: 5,
    random: true,
    database_prompts: true,
    user_prompts: null,
    user_topics: null,
  });

  const mutation = useMutation({
    mutationFn: async (data: ToxicityBatchRequest) => {
      const response = await axios.post('http://localhost:8000/toxicity-detection-batch', data);
      return response.data;
    },
    onSuccess: (data) => {
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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  return (
    <Box maxW="7xl" mx="auto" pt={5} px={{ base: 2, sm: 12, md: 17 }}>
      <Text fontSize="2xl" fontWeight="bold" mb={8}>
        Batch Toxicity Analysis
      </Text>

      <Card mb={8}>
        <CardBody>
          <form onSubmit={handleSubmit}>
            <VStack spacing={4} align="stretch">
              <FormControl>
                <FormLabel>Model Name</FormLabel>
                <Input
                  value={formData.model.name}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      model: { ...formData.model, name: e.target.value },
                    })
                  }
                />
              </FormControl>

              <FormControl>
                <FormLabel>Number of Samples</FormLabel>
                <NumberInput
                  value={formData.num_samples}
                  onChange={(_, value) =>
                    setFormData({ ...formData, num_samples: value })
                  }
                  min={1}
                  max={100}
                >
                  <NumberInputField />
                </NumberInput>
              </FormControl>

              <FormControl display="flex" alignItems="center">
                <FormLabel mb="0">Use Random Sampling</FormLabel>
                <Switch
                  isChecked={formData.random}
                  onChange={(e) =>
                    setFormData({ ...formData, random: e.target.checked })
                  }
                />
              </FormControl>

              <FormControl display="flex" alignItems="center">
                <FormLabel mb="0">Use Database Prompts</FormLabel>
                <Switch
                  isChecked={formData.database_prompts}
                  onChange={(e) =>
                    setFormData({ ...formData, database_prompts: e.target.checked })
                  }
                />
              </FormControl>

              <Button
                mt={4}
                colorScheme="blue"
                isLoading={mutation.isPending}
                type="submit"
              >
                Run Analysis
              </Button>
            </VStack>
          </form>
        </CardBody>
      </Card>

      {mutation.data && (
        <Card>
          <CardBody>
            <Text fontSize="xl" fontWeight="semibold" mb={4}>
              Results
            </Text>
            <pre style={{ whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(mutation.data, null, 2)}
            </pre>
          </CardBody>
        </Card>
      )}
    </Box>
  );
}