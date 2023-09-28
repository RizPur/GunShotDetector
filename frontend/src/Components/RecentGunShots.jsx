import React from "react";
import { Divider, ListItemButton, ListItemText, Typography } from '@mui/material';

const RecentGunShots = ({setGunShot, gunShot, flyMap, setShow}) =>{

    return(
        <>
            <ListItemButton sx={{backgroundColor: gunShot.prob > 0.5 ? 'red' : 'orange'}} 
                onClick={() => {
                setGunShot(gunShot);
                setShow(true)
                console.log(gunShot);
                flyMap(gunShot.geo[0], gunShot.geo[1], 11)
                }}>
                <ListItemText 
                primary={gunShot.location} 
                secondary={gunShot.dateTime} 
                />
                </ListItemButton>
            <Divider />
        </>
    )
}

export default RecentGunShots;