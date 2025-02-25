import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  useToast,
  Text,
  Card,
  CardBody,
  Select,
  Tag,
  TagLabel,
  TagCloseButton,
  Wrap,
  WrapItem,
} from '@chakra-ui/react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

interface BiasRequest {
  model: {
    name: string;
    description: string;
    base_url: string | null;
  };
  prompts: {
    prompt_library_path: string;
  };
  topics: string[];
}

const AVAILABLE_TOPICS = [
  'gender',
  'race',
  'religion',
  'age',
  'disability',
  'nationality',
  'appearance',
  'socioeconomic',
];

export default function BiasBatch() {
  const toast = useToast();
  const [formData, setFormData] = useState<BiasRequest>({
    model: {
      name: 'openai',
      description: 'OpenAI model for bias testing',
      base_url: null,
    },
    prompts: {
      prompt_library_path: 'path/to/prompts.json',
    },
    topics: [],
  });

  const mutation = useMutation({
    mutationFn: async (data: BiasRequest) => {
      const response = await axios.post('http://localhost:8000/bias-detection-batch', data);
      return response.data;
    },
    onSuccess: (data) => {
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

  const handleAddTopic = (topic: string) => {
    if (!formData.topics.includes(topic)) {
      setFormData({
        ...formData,
        topics: [...formData.topics, topic],
      });
    }
  };

  const handleRemoveTopic = (topic: string) => {
    setFormData({
      ...formData,
      topics: formData.topics.filter((t) => t !== topic),
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  return (
    <Box maxW="7xl" mx="auto" pt={5} px={{ base: 2, sm: 12, md: 17 }}>
      <Text fontSize="2xl" fontWeight="bold" mb={8}>
        Batch Bias Analysis
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
                <FormLabel>Prompt Library Path</FormLabel>
                <Input
                  value={formData.prompts.prompt_library_path}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      prompts: { prompt_library_path: e.target.value },
                    })
                  }
                />
              </FormControl>

              <FormControl>
                <FormLabel>Add Topics</FormLabel>
                <Select
                  placeholder="Select topic"
                  onChange={(e) => handleAddTopic(e.target.value)}
                >
                  {AVAILABLE_TOPICS.map((topic) => (
                    <option key={topic} value={topic}>
                      {topic.charAt(0).toUpperCase() + topic.slice(1)}
                    </option>
                  ))}
                </Select>
              </FormControl>

              <Wrap spacing={2}>
                {formData.topics.map((topic) => (
                  <WrapItem key={topic}>
                    <Tag size="md" borderRadius="full" variant="solid" colorScheme="blue">
                      <TagLabel>{topic}</TagLabel>
                      <TagCloseButton onClick={() => handleRemoveTopic(topic)} />
                    </Tag>
                  </WrapItem>
                ))}
              </Wrap>

              <Button
                mt={4}
                colorScheme="blue"
                isLoading={mutation.isPending}
                type="submit"
                isDisabled={formData.topics.length === 0}
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