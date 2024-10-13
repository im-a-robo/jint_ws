// src/startServer.js
const { PythonShell } = require('python-shell');

let pythonProcess;

const startPythonProcesses = () => {
    pythonProcess = PythonShell.run('./components/main.py', null, (err) => {
        if (err) {
            console.error('Error starting Python script:', err);
        } else {
            console.log('Python script started successfully');
        }
    });
};

const stopPythonProcesses = () => {
    if (pythonProcess) {
        pythonProcess.terminate();  // Terminate the process
        console.log('Python script terminated');
    }
};

module.exports = { startPythonProcesses, stopPythonProcesses };
