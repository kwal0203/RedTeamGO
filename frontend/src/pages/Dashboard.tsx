import React from 'react';
import {
  Box,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Text,
  useColorModeValue,
} from '@chakra-ui/react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface StatCardProps {
  title: string;
  stat: string;
  helpText: string;
}

function StatCard(props: StatCardProps) {
  const { title, stat, helpText } = props;
  return (
    <Stat
      px={{ base: 4, md: 8 }}
      py={'5'}
      shadow={'xl'}
      border={'1px solid'}
      borderColor={useColorModeValue('gray.800', 'gray.500')}
      rounded={'lg'}
      bg={useColorModeValue('white', 'gray.700')}
    >
      <StatLabel fontWeight={'medium'} isTruncated>
        {title}
      </StatLabel>
      <StatNumber fontSize={'2xl'} fontWeight={'medium'}>
        {stat}
      </StatNumber>
      <StatHelpText>{helpText}</StatHelpText>
    </Stat>
  );
}

export default function Dashboard() {
  const { data: healthData } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const { data } = await axios.get('http://localhost:8000/health');
      return data;
    },
  });

  return (
    <Box maxW="7xl" mx={'auto'} pt={5} px={{ base: 2, sm: 12, md: 17 }}>
      <Text
        fontSize="2xl"
        fontWeight="bold"
        mb={8}
      >
        System Dashboard
      </Text>

      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={{ base: 5, lg: 8 }}>
        <StatCard
          title={'System Status'}
          stat={healthData?.status || 'Loading...'}
          helpText={'Current system health status'}
        />
        <StatCard
          title={'Database Status'}
          stat={'Connected'}
          helpText={'Red team prompt database status'}
        />
        <StatCard
          title={'API Status'}
          stat={'Online'}
          helpText={'API endpoint availability'}
        />
      </SimpleGrid>
    </Box>
  );
}