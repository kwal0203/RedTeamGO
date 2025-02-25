import React from 'react';
import {
  Box,
  Flex,
  Text,
  Button,
  useColorModeValue,
  Stack,
  useColorMode,
} from '@chakra-ui/react';
import { MoonIcon, SunIcon } from '@chakra-ui/icons';

export default function Navbar() {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <Box
      bg={useColorModeValue('white', 'gray.900')}
      px={4}
      boxShadow="sm"
    >
      <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
        <Text
          fontSize="xl"
          fontWeight="bold"
          bgGradient="linear(to-r, cyan.400, blue.500, purple.600)"
          bgClip="text"
        >
          RedTeamGO
        </Text>

        <Flex alignItems={'center'}>
          <Stack direction={'row'} spacing={7}>
            <Button onClick={toggleColorMode}>
              {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
            </Button>
          </Stack>
        </Flex>
      </Flex>
    </Box>
  );
}