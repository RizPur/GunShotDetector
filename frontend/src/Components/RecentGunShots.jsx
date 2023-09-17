import React from "react";
import { Divider, ListItemButton, ListItemText, Typography } from '@mui/material';

const RecentGunShots = ({setGunShot, gunShot}) =>{

    return(
        <>
            <ListItemButton sx={{backgroundColor: gunShot.prob > 0.5 ? 'red' : 'orange'}} 
                onClick={() => {
                setGunShot(gunShot);
                console.log(gunShot);
                }}>
                <ListItemText 
                primary={gunShot.location} 
                secondary={gunShot.prob} 
                />
                </ListItemButton>
            <Divider />
        </>
    )
}

export default RecentGunShots;