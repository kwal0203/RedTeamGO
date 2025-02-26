import React from 'react';
import {
  Box,
  VStack,
  Link,
  useColorModeValue,
} from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';

export default function Sidebar() {
  const location = useLocation();
  const activeBg = useColorModeValue('blue.50', 'blue.900');
  const hoverBg = useColorModeValue('gray.100', 'gray.700');

  const NavItem = ({ to, children }: { to: string; children: React.ReactNode }) => {
    const isActive = location.pathname === to;
    return (
      <Link
        as={RouterLink}
        to={to}
        w="full"
        p={3}
        borderRadius="md"
        _hover={{ bg: hoverBg, textDecoration: 'none' }}
        bg={isActive ? activeBg : 'transparent'}
        fontWeight={isActive ? 'semibold' : 'normal'}
      >
        {children}
      </Link>
    );
  };

  return (
    <Box
      as="nav"
      pos="sticky"
      top="4rem"
      w="240px"
      h="calc(100vh - 4rem)"
      pt={5}
      px={4}
      overflowY="auto"
      bg={useColorModeValue('white', 'gray.900')}
      borderRight="1px"
      borderRightColor={useColorModeValue('gray.200', 'gray.700')}
    >
      <VStack spacing={2} align="stretch">
        <NavItem to="/">Dashboard</NavItem>
        <NavItem to="/realtime">Real-time Analysis</NavItem>
        <NavItem to="/toxicity-batch">Toxicity Batch</NavItem>
        <NavItem to="/bias-batch">Bias Batch</NavItem>
      </VStack>
    </Box>
  );
}
