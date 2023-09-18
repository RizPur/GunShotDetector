import React from "react";
import { Stack, Typography, TableHead, Card, CardContent} from "@mui/material";
import { Pie, Bar } from "react-chartjs-2";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import {ArcElement} from 'chart.js'
import {CategoryScale} from 'chart.js'; 
import Chart from 'chart.js/auto';


const GunChart = ({ gunShot }) => {
  
  const pieData = {
    labels: Object.keys(gunShot.probs),
    datasets: [
      {
        data: Object.values(gunShot.probs),
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
        ],
      },
    ],
  };

  return (
    <Stack spacing={2} sx={{ width: 600 }}>
        <Typography variant="h6">GunShot Details</Typography>
        <Card elevation={3} sx={{ backgroundColor: 'f9f9f9' }}>
            <CardContent>
                <Typography variant="body2">Probability: {gunShot.prob}</Typography>
                <Typography variant="body2">Parish: {gunShot.parish}</Typography>
                <Typography variant="body2">Location: {gunShot.location}</Typography>
                <Typography variant="body2">Geo: [{gunShot.geo.join(", ")}]</Typography>
            </CardContent>
        </Card>
        {console.log("Bar data: ", pieData)}
        
        {/* <TableContainer sx={{ background: 'white', borderRadius: '5px' }}>
            <Table sx={{ minWidth: 400 }}>
                <TableHead>
                    <TableRow>
                        <TableCell sx={{ fontWeight: 'bold' }}>Gun</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Probability</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                {Object.entries(gunShot.probs).map(([key, value], index) => (
                    <TableRow key={index} sx={{ '&:nth-of-type(odd)': { background: '#f2f2f2' } }}>
                    <TableCell sx={{ fontWeight: 'bold' }}>{key}</TableCell>
                    <TableCell>{value}</TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
        </TableContainer> */}
        <Bar data={pieData} />
     </Stack>
  );
};

export default GunChart;
