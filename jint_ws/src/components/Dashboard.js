// Dashboard.js
import React, { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Input,
  Text,
  Button,
} from '@chakra-ui/react';
import Analytic from './Analytic';

export const Dashboard = () => {
  const [patients, setPatients] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPatients = async () => {
      const therapistId = 1; // Example therapist ID, you can set this dynamically
      const { data, error } = await supabase
        .from('patients')
        .select('*');
        //.eq('therapist_id', therapistId);

      if (error) {
        console.error('Error fetching patients:', error);
      } else {
        setPatients(data);
      }
    };

    fetchPatients();
  }, []);

  // Filter patients based on the search query
  const filteredPatients = patients.filter((patient) =>
    patient.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Navigate to the specific patient page
  const handleRowClick = (id) => {
    navigate(`/patient/${id}`);
  };

  return (
    <Box p={5}>

<Button
      onClick={() => {
        fetch('http://127.0.0.1:5000/start-thread', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
          alert(data.status);  // Show alert with the thread status from the server
        })
        .catch(error => {
          console.error('Error:', error);  // Log any errors
        });
      }}
    >
  Start Python Thread
</Button>

<Button
      onClick={() => {
        fetch('http://127.0.0.1:5000/stop-thread', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
          alert(data.status);  // Show alert with the thread status from the server
        })
        .catch(error => {
          console.error('Error:', error);  // Log any errors
        });
      }}
    >
  Stop Python Thread
</Button>


      {/* Header with teal color */}
      <Box bg="teal.500" p={4} mb={4} color="white" borderRadius="md">
        <Text fontSize="2xl" fontWeight="bold" textAlign="center">
          Patient Dashboard
        </Text>
      </Box>

      {/* Search input */}
      <Input
        placeholder="Search by name..."
        mb={4}
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)} // Update search query
      />

      {/* Patients table */}
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Name</Th>
            <Th>Email</Th>
            <Th>Notes</Th>
          </Tr>
        </Thead>
        <Tbody>
          {filteredPatients.length > 0 ? (
            filteredPatients.map((patient) => (
              <Tr
                key={patient.id}
                cursor="pointer"
                onClick={() => handleRowClick(patient.id)} // Handle row click
                _hover={{ backgroundColor: 'teal.50' }} // Add hover effect with light teal color
              >
                <Td>{patient.id}</Td>
                <Td>{patient.name}</Td>
                <Td>{patient.email || 'No email available'}</Td>
                <Td>{patient.notes || 'No notes available'}</Td>
              </Tr>
            ))
          ) : (
            <Tr>
              <Td colSpan={4} textAlign="center">
                No patients found
              </Td>
            </Tr>
          )}
        </Tbody>
      </Table>
      <Analytic />
    </Box>
  );
};
