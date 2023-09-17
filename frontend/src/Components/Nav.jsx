import React from 'react';
import BottomNavigation from '@mui/material/BottomNavigation';
// import BottomNavigationAction from '@mui/material/BottomNavigationAction';
import { Divider, List, Paper, Box } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import '../App.css'
import RecentGunShots from './RecentGunShots';


const darkTheme = createTheme({ palette: { mode: 'dark' } });
const lightTheme = createTheme({ palette: { mode: 'light' } });

const Nav = ({gunShots, setGunShot, flyMap}) =>{

    return (
        <div id="b-bar">
            <ThemeProvider theme={darkTheme}>
                <Box>
                    <Paper sx={{ position: 'fixed', maxWidth: '90vh', bottom: 0, left: 5}} elevation={3}>
                        <Paper sx={{ maxHeight: '85vh', overflow: 'auto' }} elevation={3}>
                            <List>
                                {gunShots.map(gunShot =>(
                                    <RecentGunShots key={gunShot.id} gunShot={gunShot} setGunShot={setGunShot} flyMap={flyMap}/>
                                ))}
                            </List>
                        </Paper>
                    </Paper>
                </Box>
            </ThemeProvider>
        </div>
    )
}

export default Nav