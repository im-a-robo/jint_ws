import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';
import {
  Box,
  Button,
  Heading,
  Text,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Input,
  Avatar,
  useToast,
} from '@chakra-ui/react';

export const Patient = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [patient, setPatient] = useState(null);
  const [recordings, setRecordings] = useState([]);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    const fetchPatientDetails = async () => {
      const { data, error } = await supabase
        .from('patients')
        .select('*')
        .eq('id', id)
        .single();

      if (error) {
        console.error('Error fetching patient details:', error);
        toast({
          title: 'Error fetching patient details',
          description: error.message,
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      } else {
        setPatient(data);
      }
      setLoading(false);
    };

    const fetchRecordings = async () => {
      const { data, error } = await supabase
        .from('user_recordings')
        .select('*')
        .eq('patient_id', id);

      if (error) {
        console.error('Error fetching recordings:', error);
        toast({
          title: 'Error fetching recordings',
          description: error.message,
          status: 'error',
          duration: 3000,
          isClosable: true,
        });
      } else {
        setRecordings(data);
      }
    };

    fetchPatientDetails();
    fetchRecordings();
  }, [id]);

  const moveToAnalytics = (recordingId) => {
    navigate('/analytic', { state: { recordingId } }); // Pass the recording ID as state
    console.log(`Viewing analytics for recording ID: ${recordingId}`);
  };

  if (loading) return <Text>Loading...</Text>;

  return (
    <Box p={5}>
      {patient && (
        <>
          <Box display="flex" alignItems="center" mb={4}>
            <Avatar name={patient.name} size="lg" />
            <Box ml={4}>
              <Heading size="md">{patient.name}</Heading>
              <Text>Email: {patient.email}</Text>
            </Box>
            <Button
              colorScheme="red"
              ml="auto"
              onClick={() => navigate('/video')}
            >
              Start New Recording
            </Button>
          </Box>

          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Timestamp</Th>
                <Th>Notes</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            <Tbody>
              {recordings.length > 0 ? (
                recordings.map((recording) => (
                  <Tr key={recording.id}>
                    <Td>{new Date(recording.start_time).toLocaleString()}</Td>
                    <Td>
                      <Input
                        defaultValue={recording.notes}
                        onChange={(e) =>
                          console.log(`Update notes for recording ID ${recording.id}: ${e.target.value}`)
                        }
                      />
                    </Td>
                    <Td>
                      <Button
                        colorScheme="teal"
                        onClick={() => moveToAnalytics(recording.id)} // Pass the recording ID
                      >
                        View Analytics
                      </Button>
                    </Td>
                  </Tr>
                ))
              ) : (
                <Tr>
                  <Td colSpan={3} textAlign="center">
                    No recordings found
                  </Td>
                </Tr>
              )}
            </Tbody>
          </Table>
        </>
      )}
    </Box>
  );
};
