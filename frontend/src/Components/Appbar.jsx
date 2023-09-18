import React from "react";
import {Button, Box, AppBar, Toolbar, Typography} from '@mui/material'


const Appbar = ({flyMap, setShow})=>{
    return (
        <div id="app-bar">
            <Box sx={{ flexGrow: 1 }}>
            <AppBar position='static'>
                <Toolbar sx={{minHeight: '48px'}}>
                <Button variant='contained' sx={{backgroundColor:'orange'}} onClick={()=>{
                    flyMap(18,-77,9)
                }}>Fly Away</Button>
                <Button variant='contained' sx={{backgroundColor:'green'}} onClick={()=>{
                   setShow(true)
                }}>Details</Button>
                <Box sx={{ flexGrow: 1 }}></Box>
                <Typography
                    sx={{
                        display: 'inline',
                        fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
                        fontWeight: 'bold',
                        textShadow: '2px 2px 4px #000000',
                        color: '#FFFFFF',
                        padding: '5px',
                        borderRadius: '5px',
                    }}
                    component="span"
                    variant="h3"
                    color="text.primary"
                    >
                    Jamaica Gunshot Alert System
                </Typography>
                <Box sx={{ flexGrow: 1 }}></Box>
                </Toolbar>
            </AppBar>
            </Box>
        </div>
    )
}

export default Appbar