// src/components/EmotionChart.js

import React, { useEffect, useRef } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js'; // Import Chart and registerables
import 'chartjs-adapter-date-fns'; // Import the date adapter

// Register all components, including time scale
Chart.register(...registerables);

const Analytic = () => {
    const chartRef = useRef(null);

    const data = {
        labels: [], // Fill with timestamps
        datasets: [
            {
                label: 'Happy',
                data: [], // Fill with happy data
                borderColor: 'yellow',
                borderWidth: 2,
            },
            {
                label: 'Sad',
                data: [], // Fill with sad data
                borderColor: 'blue',
                borderWidth: 2,
            },
            // Add other emotions here
        ],
    };

    const options = {
        scales: {
            x: {
                type: 'time', // Ensure you're using time scale
                time: {
                    unit: 'minute', // Change unit according to your data
                },
                title: {
                    display: true,
                    text: 'Time (HH:MM)',
                },
            },
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Emotion Percentage (%)',
                },
            },
        },
    };

    useEffect(() => {
        // Cleanup function to destroy chart instance if it exists
        return () => {
            if (chartRef.current) {
                chartRef.current.destroy();
            }
        };
    }, []);

    return (
        <div>
            <Line ref={chartRef} data={data} options={options} />
        </div>
    );
};

export default Analytic;
