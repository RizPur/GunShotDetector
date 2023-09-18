import React from "react";
import { Stack, Typography, TableHead, Card, CardContent} from "@mui/material";
import { Bar } from "react-chartjs-2";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';

const GunChart = ({ gunShot }) => {

  return (
    <Stack spacing={2} sx={{width:600}}>
        <Typography variant="h6">GunShot Details</Typography>
        <Card elevation={3} sx={{backgroundColor: 'f9f9f9'}}>
            <CardContent>
                {/* <Typography variant="body2">ID: {gunShot.ID}</Typography> */}
                <Typography variant="body2">Probability: {gunShot.prob}</Typography>
                <Typography variant="body2">Parish: {gunShot.parish}</Typography>
                <Typography variant="body2">Location: {gunShot.location}</Typography>
                <Typography variant="body2">Geo: [{gunShot.geo.join(", ")}]</Typography>
            </CardContent>
        </Card>
        
        <TableContainer sx={{ background: 'white', borderRadius: '5px' }}>
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
        </TableContainer>

     </Stack>


  );
};

export default GunChart;
