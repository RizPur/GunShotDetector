import {MapContainer, TileLayer} from 'react-leaflet'

const Jamaica = ({centers}) => {
    return (
        <MapContainer
            center={centers.ja}
            zoom={10}
            style={{width: '100vw', height: '100vh'}}
            scrollWheelZoom={false}
            zoomControl={false}>
                <TileLayer
           url="https://api.maptiler.com/maps/basic/256/{z}/{x}/{y}.png?key=73p7aIRQ0vUQYQlwBn1Q" //different map
            />

        </MapContainer>
    )
}

export default Jamaica