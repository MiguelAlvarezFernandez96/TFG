<template>
    <div style="padding: 10px; display: flex; justify-content: center;">
        <div id="map"></div>
    </div>
</template>

<script>
import { defineComponent, onMounted, inject, ref, require } from 'vue'
import leaflet from 'leaflet'

export default defineComponent({
    setup () {

        let client = inject('mqttClient');
        let emitter = inject('emitter');

        let map;
        let direction;
        let selectedLevel;
        let state;

        let interval;

        let drone;
        let northLine;
        let southLine;
        let westLine;
        let eastLine;

        let northLabel;
        let southLabel;
        let eastLabel;
        let westLabel;

        let practicePointLat = 41.2765003;
        let practicePointLong = 1.9889760;
        let practicePoint = [practicePointLat, practicePointLong];

        let northPoint;
        let southPoint;
        let eastPoint;
        let westPoint;
        let northIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow; margin-left: 2px;'>N</b></div>"})
        let southIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow; margin-left: 2px;'>S</b></div>"})
        let eastIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow;'>E</b></div>"})
        let westIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow;'>W</b></div>"})

        let droneLabLimits = [[41.2764151, 1.9882914],[41.2762170, 1.9883551],[41.2763733, 1.9890491],[41.2765582, 1.9889881]];
        let obstacle1 = [[41.2764408, 1.9885938],[41.2764368, 1.9886494],[41.2763385, 1.9886407],[41.2763450, 1.9885878]];
        let obstacle21 = [[41.2765219, 1.9888506],[41.2764065, 1.9888902],[41.2763924, 1.9888600],[41.2765669, 1.9887990]];
        let obstacle22 = [[41.2764287, 1.9887453],[41.2763123, 1.9888077],[41.2763032, 1.9887460],[41.2764267, 1.9887111]];
        let obstacle23 = [[41.2764569, 1.9885515],[41.2763461, 1.9886903],[41.2763274, 1.9886535],[41.2764473, 1.9885274]];
        
        function setDirection(code){
            if (code == 0){
                direction = "Stop";
            }
            else if (code == 1){
                direction = "North";
            }
            else if (code == 2){
                direction = "South";
            }
            else if (code == 3){
                direction = "East";
            }
            else if (code == 4){
                direction = "West";
            }
            else if (code == 5){
                direction = "Drop";
            }
            else if (code == 6){
                direction = "Return";
            }
            //emitter.emit('direction',{direction: direction});
       }

       function inside(point, vs) {
            // ray-casting algorithm
            
            var x = point[0], y = point[1];
            
            var inside = false;
            for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
                var xi = vs[i][0], yi = vs[i][1];
                var xj = vs[j][0], yj = vs[j][1];
                
                var intersect = ((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
                if (intersect) { 
                    inside = !inside;
                }
            }
            
            return inside;
        }

       function paintDrone(){
            if(drone!=undefined){
                drone.remove(map);
            }
            if(northLine!=undefined){
                northLine.remove(map);
            }
            if(southLine!=undefined){
                southLine.remove(map);
            }
            if(eastLine!=undefined){
                eastLine.remove(map);
            }
            if(westLine!=undefined){
                westLine.remove(map);
            }
            if(northLabel!=undefined){
                northLabel.remove(map);
            }
            if(southLabel!=undefined){
                southLabel.remove(map);
            }
            if(eastLabel!=undefined){
                eastLabel.remove(map);
            }
            if(westLabel!=undefined){
                westLabel.remove(map);
            }
            
            drone = leaflet.circle(practicePoint, 0.8, {stroke: false, fill: true, fillColor: "red", fillOpacity: 1}).addTo(map);
            northPoint = [practicePointLat + 0.00003, practicePointLong + 0];
            southPoint = [practicePointLat - 0.00003, practicePointLong + 0];
            eastPoint = [practicePointLat + 0, practicePointLong + 0.00004];
            westPoint = [practicePointLat + 0, practicePointLong - 0.00004];
            northLine = leaflet.polyline([practicePoint, northPoint], {color: 'red'}).addTo(map);
            southLine = leaflet.polyline([practicePoint, southPoint], {color: 'red'}).addTo(map);
            eastLine = leaflet.polyline([practicePoint, eastPoint], {color: 'red'}).addTo(map);
            westLine = leaflet.polyline([practicePoint, westPoint], {color: 'red'}).addTo(map);
            northLabel = leaflet.marker( northPoint, {
                icon: northIcon
            }).addTo(map);
            southLabel = leaflet.marker( southPoint, {
                icon: southIcon
            }).addTo(map);
            eastLabel = leaflet.marker( eastPoint, {
                icon: eastIcon
            }).addTo(map);
            westLabel = leaflet.marker( westPoint, {
                icon: westIcon
            }).addTo(map);
       }

       const R = 6378.1;
       const d = 0.0005;

       function movePoint(){
            let bearing = null;
            if (direction == "North"){
                bearing = 0;
            }
            else if (direction == "South"){
                bearing = Math.PI;
            }
            else if (direction == "East"){
                bearing = Math.PI/2;
            }
            else if (direction == "West"){
                bearing = 3*Math.PI/2;
            }
            if (bearing != null){             

                let lat = practicePointLat*Math.PI/180;
                let lon = practicePointLong*Math.PI/180;

                practicePointLat = (Math.asin(
                    Math.sin(lat) * Math.cos(d / R)
                    + Math.cos(lat) * Math.sin(d / R) * Math.cos(bearing)
                ))*180/Math.PI;

                practicePointLong = (lon + Math.atan2(
                    Math.sin(bearing) * Math.sin(d / R) * Math.cos(lat),
                    Math.cos(d / R) - Math.sin(lat) * Math.sin(practicePointLat),
                ))*180/Math.PI;

                practicePoint = [practicePointLat, practicePointLong];
            }
            // estic canviant el practice point encara que estigui fora dels droneLabLimits, canviarho a dins del if
            if(selectedLevel=="Basico" && inside(practicePoint, droneLabLimits)){
                paintDrone();
            }
            else if(selectedLevel=="Medio" && inside(practicePoint, droneLabLimits) && !inside(practicePoint, obstacle1)){
                paintDrone();
            }
            else if(selectedLevel=="Avanzado" && inside(practicePoint, droneLabLimits) && !inside(practicePoint, obstacle21) && !inside(practicePoint, obstacle22) && !inside(practicePoint, obstacle23)){
                paintDrone();
            }
       }

       function startMoving(){
            interval = setInterval(() => {
                movePoint();
            }, 3000);
       }

       function stopMoving(){
            clearInterval(interval);
       }

        onMounted (() => {
            
            map = leaflet.map('map').setView([41.276386, 1.9886], 20); //coordenadas del campus, es posa en un objecte amb id 'map' que posem a la div, el 19 i el maxZoom es per allunyar i apropar
                        
           // MapBox
           let token = "pk.eyJ1Ijoiam9hbmEtb3AiLCJhIjoiY2xkdTRtOHhmMDJjaDN2bXY0Zjl3b2pqeCJ9.6zfF7e0G7vK8Vyy4YE8mxw";
           leaflet.tileLayer('https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token='+token, {
                maxZoom: 20,
                attribution: 'MapBox'
            }).addTo(map);
           // map.on("click",onMapClick); // associem el event click a la funcio onMapClick
           // map.on("mousemove",onMapOver); // passar el ratoli per sobre el mapa
           // map.on("contextmenu",onRightClick); //context menu es el click del boto dret del ratoli
           let droneLabPolygon = leaflet.polygon(droneLabLimits, {color: 'white'}).addTo(map);           

           paintDrone();
           
           emitter.on('videoCaptureCircus', (cap) => {
                if(cap.capturing && cap.state !="flying"){
                    startMoving();
                }
                else if(!cap.capturing && cap.state != "returning"){
                    stopMoving();
                }
                state = cap.state;
            });

            emitter.on ('selectedLevelCircus', (data) => {
                selectedLevel = data.level;                
                if(selectedLevel=="Medio"){
                    let obstacle1Polygon = leaflet.polygon(obstacle1, {color: 'blue'}).addTo(map);
                }
                else if(selectedLevel=="Avanzado"){
                    let obstacle21Polygon = leaflet.polygon(obstacle21, {color: 'blue'}).addTo(map);
                    let obstacle22Polygon = leaflet.polygon(obstacle22, {color: 'blue'}).addTo(map);
                    let obstacle23Polygon = leaflet.polygon(obstacle23, {color: 'blue'}).addTo(map);
                }                                   
            })

            emitter.on('autopilotPositionCircus', (data) => {
                practicePointLat = data.lat;
                practicePointLong = data.long;
                practicePoint = [practicePointLat, practicePointLong];
                paintDrone();
            })

           client.on('message', (topic,message) => {
                console.log(topic)
                if (topic=="imageService/droneCircusWebApp/code" && state == "practising"){
                    setDirection(message);
                    emitter.emit('directionCircus', {'direction': direction});
                    movePoint(); // crec que s'ha de treure
                }
                else if (topic=="imageService/mobileApp/code" && state == "practising"){
                    setDirection(message);
                    emitter.emit('directionCircus', {'direction': direction});
                    movePoint(); // crec que s'ha de treure
                }
                else if(topic=="imageService/droneCircusWebApp/code" && state == "flying"){
                    setDirection(message);
                    emitter.emit('directionCircus', {'direction': direction});
                }
                else if(topic=="imageService/mobileApp/code" && state == "flying"){
                    setDirection(message);
                    emitter.emit('directionCircus', {'direction': direction});
                }
           })
           
       })
       
        return {
            client,
            setDirection,
            practicePoint,
            northPoint,
            selectedLevel
        }
    }
})
</script>

<style scoped>

    #map {
        width: 70%;
        height: 360px;
        border-style: solid;
        z-index: 1;
    }
    .mylabel{
        background-color: black;
        width: 50px;  
    }
</style>