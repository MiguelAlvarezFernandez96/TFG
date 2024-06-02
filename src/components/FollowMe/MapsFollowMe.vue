<template>
    <div style="margin-top: 2%;">
        <div>
            <div style="display:flex">
                <div id="map"></div>                
            </div>                             
        </div> 
        <ChoosePlayerFollowMe v-if="choosingPlayer" @close = "close()" :players="playersToBeAssigned"></ChoosePlayerFollowMe>
    </div>
</template>

<script>
import {onMounted, inject, ref } from 'vue'
import leaflet from 'leaflet'
import ChoosePlayerFollowMe from './ChoosePlayerFollowMe.vue'
import Swal from 'sweetalert2'

export default {

    components: {
        ChoosePlayerFollowMe
    },

    setup (props, context) {      

        let map;
        let popup = leaflet.popup();
        const emitter = inject('emitter');
        let client = inject('mqttClient');    
        
        // Variables d'estat
        let state = "disconnected"
        let canConnect = false;
        
        // Variables dibuix dron
        let drone;
        let northLine;
        let southLine;
        let westLine;
        let eastLine;
        let practicePointLat = 41.2765003;
        let practicePointLong = 1.9889760;
        let practicePoint = [practicePointLat, practicePointLong];
        let northPoint;
        let southPoint;
        let eastPoint;
        let westPoint;
        let northIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow; margin-left: 2px;'>N</b></div>"});
        let southIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow; margin-left: 2px;'>S</b></div>"});
        let eastIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow;'>E</b></div>"});
        let westIcon = leaflet.divIcon({className: 'mylabel', html: "<div style='width: 50;'><b style='color:yellow;'>W</b></div>"});
        let northLabel;
        let southLabel;
        let eastLabel;
        let westLabel;

        // Variables limits dronelab
        
        let droneLab = [[41.27643580, 1.98821960],[41.27619490, 1.98833760],[41.27636320, 1.98911820],[41.27658190, 1.98901760]];
        let droneLabLimits = [[41.2762327, 1.9883584],[41.2764141, 1.9882706],[41.2765547, 1.9889887],[41.2763788, 1.9890692]]; //començo baix a l'esquerra, dalt esquerra, dalt dreta, baix dreta
        //recta 1: y = mx + n; 41.2762049 = m1.9883443 + n; 41.2764327= m1.9882290 + n; -0,0002278 = 0,0001153m; m = -1,9757155247181266261925; n = 37,34825779800520381613191;
        let recta01m = (droneLabLimits[0][0]-droneLabLimits[1][0])/(droneLabLimits[0][1]-droneLabLimits[1][1]);
        let recta01n = droneLabLimits[0][0] - recta01m*droneLabLimits[0][1];

        let recta12m = (droneLabLimits[1][0]-droneLabLimits[2][0])/(droneLabLimits[1][1]-droneLabLimits[2][1]);
        let recta12n = droneLabLimits[1][0] - recta12m*droneLabLimits[1][1];

        let recta23m = (droneLabLimits[2][0]-droneLabLimits[3][0])/(droneLabLimits[2][1]-droneLabLimits[3][1]);
        let recta23n = droneLabLimits[2][0] - recta23m*droneLabLimits[2][1];

        let recta30m = (droneLabLimits[3][0]-droneLabLimits[0][0])/(droneLabLimits[3][1]-droneLabLimits[0][1]);
        let recta30n = droneLabLimits[3][0] - recta30m*droneLabLimits[3][1];

        // Variables jugadors

        let waypoints = [];
        let players = [];        
        let playersMarkers = [];
        let playersTurn = ref("");
        let fixedPoints = [[41.2763486,1.9882531],[41.2764405, 1.9882089], [41.2765622,1.9888801],[41.2765925,1.9890236],[41.2764972,1.9890632],[41.2763632,1.9891322],[41.2762856,1.9887809],[41.2761835, 1.9883259]]
        let fixedPointsMarkers = [];    
        let choosingPlayer = ref(false);
        let indexPointChoosing = 0;
        let playersToBeAssigned = ref([]) 
        let followingName;

        // Intervals
        let intervalYourTurn;
        let intervalGoToWaypoint;
           

        onMounted (() => {
            let b = 0;
            
            map = leaflet.map('map').setView([41.276386992722706, 1.988712064955474], 19); //coordenadas del campus, es posa en un objecte amb id 'map' que posem a la div, el 19 i el maxZoom es per allunyar i apropar
                          
            // MapBox
            let token = "pk.eyJ1Ijoiam9hbmEtb3AiLCJhIjoiY2xkdTRtOHhmMDJjaDN2bXY0Zjl3b2pqeCJ9.6zfF7e0G7vK8Vyy4YE8mxw";
            leaflet.tileLayer('https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token='+token, {
                 maxZoom: 21,
                 minZoom: 16,
                 attribution: 'MapBox'
             }).addTo(map);

            leaflet.polygon(droneLab, {color: 'white'}).addTo(map);
            paintDrone();
            
            // Loop to add fixed points in map
            for(let i = 0; i<fixedPoints.length; i++){
                fixedPointsMarkers.push(leaflet.marker(fixedPoints[i]).on('click', onMarkerClick).addTo(map))
            }

            emitter.on('newPlayerFollowMe', (data) => {
                players.push({name: data, point: [], marker: undefined});
                playersToBeAssigned.value.push(data);
            })          

            // quan no tenim gps
            emitter.on('playerChosenFollowMe', (data) => {                
                for(let i = 0; i<players.length; i++){
                    if(players[i].name == data.player){
                        players[i].point = fixedPoints[indexPointChoosing];
                        players[i].marker = fixedPointsMarkers[indexPointChoosing].bindTooltip(data.player, {direction: 'center', permanent: true})
                    }
                }
                indexPointChoosing = 0;
                if(canConnect == false){
                    context.emit("canConnect"); 
                    canConnect = true;
                }
                              
            })
    

            client.subscribe("+/dashboardFollowme/#");

            client.on('message', (topic, message) => {
                console.log(topic)
                if(topic=="autopilotService/dashboardFollowme/telemetryInfo"){                    
                    let telemetryInfo = JSON.parse(message);
                    console.log(telemetryInfo);
                    practicePointLat = telemetryInfo.lat;
                    practicePointLong = telemetryInfo.lon;
                    practicePoint = [practicePointLat, practicePointLong];                    
                    paintDrone();  
                    
                    if(state=="disconnected" || state=="onHearth"){
                        if(telemetryInfo.state == 'connected' || telemetryInfo.state == 'onHearth')
                        context.emit('connected');
                        state = 'connected';
                    }
                    else if(state=="connected" || state=="onHearth"){
                        if(telemetryInfo.state == "flying"){
                            context.emit('flying');
                            state = 'flying';
                            playersTurn.value = players[0].name
                            client.publish('dashboardFollowme/mobileApp/yourTurn/'+players[0].name,'')                                                        
                            resendYourTurn(players[0].name);
                        }                        
                    }
                    else if(state=="flying" && telemetryInfo.state == "returningHome" ){
                        context.emit('returning');
                        state = 'returning';
                    }
                    else if(state=="returning" && telemetryInfo.state == "onHearth"){
                        context.emit('onHearth');
                        state = 'onHearth';
                    }                    
                }

                else if(topic=="mobileApp/dashboardFollowme/position"){
                    let messageJSON = JSON.parse(message);
                    if(messageJSON['position']!=undefined && messageJSON['player']!=undefined){
                        updatePoint(messageJSON['player'], messageJSON['position']);
                        console.log(messageJSON['position'])
                        if(canConnect == false){
                            context.emit("canConnect"); 
                            canConnect = true;
                        }
                    }                                        
                }

                else if(topic == "mobileApp/dashboardFollowme/following"){
                    console.log(message.toString())
                    for(let i = 0; i <players.length; i++){
                        if(players[i].name == message.toString()){
                            goToPoint(i)
                            emitter.emit('followingFollowMe', message.toString())
                            followingName = message.toString();
                            clearInterval(intervalYourTurn);
                        }
                    }
                    
                }

                else if(topic=="autopilotService/dashboardFollowme/waypointReached"){
                    client.publish('dashboardFollowme/mobileApp/yourTurn/'+followingName,'')
                    clearInterval(intervalGoToWaypoint);
                    resendYourTurn(followingName);
                }

                
            })
        })

        function paintDrone(){

            quitDronePainting();
            
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

        

        function quitDronePainting(){
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
        }

       
        function goToPoint(index){
            let waypoint = players[index].point;
            let newRectam;
            let newRectan;
            let sector;
            let intersectionWaypoint;
            let newlat;
            let newlon;
            console.log('inside ' + index)
            if(waypoint[0]<(recta01m*waypoint[1]+recta01n)){
                if(waypoint[0]>(recta12m*waypoint[1]+recta12n)){
                    sector = 2;
                    intersectionWaypoint = droneLabLimits[1];
                }
                else if(waypoint[0]<(recta30m*waypoint[1]+recta30n)){
                    sector = 8;
                    intersectionWaypoint = droneLabLimits[0];
                }
                else{
                    sector = 1;
                    newRectam = -1/recta01m;
                    newRectan = waypoint[0]-newRectam*waypoint[1];
                    newlon = (newRectan-recta01n)/(recta01m-newRectam);
                    newlat = recta01m*newlon + recta01n;
                    intersectionWaypoint = [newlat, newlon];
                }
            }
            else if(waypoint[0]>(recta23m*waypoint[1]+recta23n)){
                if(waypoint[0]>(recta12m*waypoint[1]+recta12n)){
                    sector = 4;
                    intersectionWaypoint = droneLabLimits[2];
                }
                else if(waypoint[0]<(recta30m*waypoint[1]+recta30n)){
                    sector = 6;
                    intersectionWaypoint = droneLabLimits[3];
                }
                else{
                    sector = 5;
                    newRectam = -1/recta23m;
                    newRectan = waypoint[0]-newRectam*waypoint[1];
                    newlon = (newRectan-recta23n)/(recta23m-newRectam);
                    newlat = recta23m*newlon + recta23n;
                    intersectionWaypoint = [newlat, newlon];
                }
            }
            else if(waypoint[0]>(recta12m*waypoint[1]+recta12n)){
                sector = 3;
                newRectam = -1/recta12m;
                newRectan = waypoint[0]-newRectam*waypoint[1];
                newlon = (newRectan-recta12n)/(recta12m-newRectam);
                newlat = recta12m*newlon + recta12n;
                intersectionWaypoint = [newlat, newlon];
            }
            else if(waypoint[0]<(recta30m*waypoint[1]+recta30n)){
                sector = 7;
                newRectam = -1/recta30m;
                newRectan = waypoint[0]-newRectam*waypoint[1];
                newlon = (newRectan-recta30n)/(recta30m-newRectam);
                newlat = recta30m*newlon + recta30n;
                intersectionWaypoint = [newlat, newlon];
            }
            else if(inside(waypoint, droneLabLimits)){
                sector = 0;
                intersectionWaypoint = waypoint;
            }
            else {
                sector = -1;
            }
             
            if(sector!=-1){
                let heading;
                if(sector!=0){
                    let headingCos = (180/Math.PI)*Math.acos((waypoint[0]-intersectionWaypoint[0])/Math.sqrt(Math.pow((waypoint[0]-intersectionWaypoint[0]),2)+Math.pow((waypoint[1]-intersectionWaypoint[1]),2)));
                    let headingSin = (180/Math.PI)*Math.asin((waypoint[1]-intersectionWaypoint[1])/Math.sqrt(Math.pow((waypoint[0]-intersectionWaypoint[0]),2)+Math.pow((waypoint[1]-intersectionWaypoint[1]),2)));
                         
                    if(waypoint[1]-intersectionWaypoint[1] > 0){ // 0 a 180
                        heading = headingCos;
                    }
                    else if(waypoint[1]-intersectionWaypoint[1] < 0){ // 180 a 360
                        heading = 360 - headingCos;
                    } 
                }
                else{
                    heading = 0;
                }
                let waypointJSON = {    
                    waypoint:{
                        lat: intersectionWaypoint[0],
                        lon: intersectionWaypoint[1]
                    },   
                    heading: heading           
                }
                console.log(waypointJSON)
                client.publish('dashboardFollowme/autopilotService/goToWaypoint',JSON.stringify(waypointJSON)) 
                resendGoToWaypoint(JSON.stringify(waypointJSON));               
            }
        }         

        function onMarkerClick(e){
            let found = false;
            if(indexPointChoosing == 0){
                while(!found){
                    if(fixedPoints[indexPointChoosing][0] == e.latlng.lat && fixedPoints[indexPointChoosing][1] == e.latlng.lng){
                        found = true;                    
                    }
                    else{
                        indexPointChoosing++;
                    }
                }
                if(found){
                    let alreadyAssigned = false
                    playersToBeAssigned.value = [];
                    for(let i = 0; i<players.length; i++){
                        if(players[i].point == fixedPoints[indexPointChoosing]){
                            alreadyAssigned = true;
                        }
                        console.log(players)
                        if(players[i].point.length == 0){
                            playersToBeAssigned.value.push(players[i].name)
                        }
                    }
                    if(!alreadyAssigned ){
                        if(playersToBeAssigned.value.length != 0){
                            choosingPlayer.value = true;
                        }
                        else{
                            Swal.fire("No players left to assign")
                            indexPointChoosing = 0;
                        }
                    }
                    else{
                        Swal.fire("This point is already assigned")
                        indexPointChoosing = 0;
                    }                
                }
            }
            

        }

        function close(){
            choosingPlayer.value = false;
            indexPointChoosing = 0;
        }

        function resendYourTurn(name){
            let seconds = 0;
            intervalYourTurn = setInterval(() => {
                seconds = seconds + 1;
                if(seconds == 60){
                    client.publish('dashboardFollowme/mobileApp/yourTurn/'+name,'');
                    seconds = 0;
                }
            }, 1000);
        }

        function resendGoToWaypoint(message){
            let seconds = 0;
            let first = true;
            intervalGoToWaypoint = setInterval(() => {
                seconds = seconds + 1;
                if(first == true){
                    if(seconds == 120){
                        client.publish('dashboardFollowme/autopilotService/goToWaypoint',message);
                        seconds = 0;
                        first = false;
                        console.log('resending goToWaypoint')
                    }
                } 
                else{
                    if(seconds == 60){
                        client.publish('dashboardFollowme/autopilotService/goToWaypoint',message);
                        seconds = 0;
                        console.log('resending goToWaypoint')
                    }
                }               
                
            }, 1000);
        }

        function updatePoint(username,waypoint){
            for(let i = 0; i < players.length; i++){
                if(username == players[i].name){
                    players[i].point = waypoint;                        
                    paintPoint(i);
                }
                
            }
            
            
        }

        function paintPoint(index){
            if(players[index].marker == undefined){
                players[index].marker = leaflet.marker(players[index].point).addTo(map).bindTooltip(players[index].name, {direction: 'center', permanent: true})
            }
            else{
                players[index].marker.remove(map);
                players[index].marker = leaflet.marker(players[index].point).addTo(map).bindTooltip(players[index].name, {direction: 'center', permanent: true})
            }            
            
        }

        return {
            map,
            popup,
            choosingPlayer,
            playersToBeAssigned,
            close
        }
    }
}
</script>

<style>

#map {  
    width: 100%;
    height: 600px;
    border-style: solid;
    z-index: 1;
}

.my_labels{
    background-color: white;
}
</style>