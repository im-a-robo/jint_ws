// Dashboard.js
import React, { useState, useEffect } from 'react';
import { supabase } from '../supabaseClient';
import { Link } from 'react-router-dom';
import {
  Box,
  Button,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Input,
} from '@chakra-ui/react';

const Dashboard = () => {
  const [patients, setPatients] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

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

  const handleAction = (id) => {
    console.log(`Action for patient ID: ${id}`);
    // Implement your action logic here (e.g., edit, delete)
  };

  // Filter patients based on the search query
  const filteredPatients = patients.filter((patient) =>
    patient.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Box p={5}>
      <h1>Dashboard</h1>
      <Input
        placeholder="Search by name..."
        mb={4}
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)} // Update search query
      />
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Name</Th>
            <Th>Notes</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {filteredPatients.length > 0 ? (
            filteredPatients.map((patient) => (
              <Tr key={patient.id}>
                <Td>{patient.id}</Td>
                <Td>{patient.name}</Td>
                <Td>{patient.notes || 'No notes available'}</Td>
                <Td>
                  <Button colorScheme="teal" onClick={() => handleAction(patient.id)}>
                    Action
                  </Button>
                </Td>
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
    </Box>
  );
};

export default Dashboard;
