<template>
    <div style="background-color: #EDF4F2; display: flex; padding-top: 15px; height: auto;">
        <div style="padding-left: 5%; width: 40%;">
            <div>
                <ButtonsDroneCircus @close="close" @selectLevel="showLevelSelector" @practice="practice" @connect="selectConnectionMode" @stopPractice="stopPractice" @arm="arm" @takeoff="takeoff" @returnHome="returnHome" @disconnect="disconnect"></ButtonsDroneCircus>
            </div>
            <div>
                <InstructionsDroneCircus></InstructionsDroneCircus>
            </div>        
        </div>
        <div style="width: 60%">
            <div style="padding=5%">
                <MapDroneCircus></MapDroneCircus>
            </div>
            <div> 
                <DetectorDroneCircus></DetectorDroneCircus>
            </div>
        </div>
        <LevelSelectorDroneCircus v-if="levelSelectorShowing" @close="levelSelectorShowing=false"></LevelSelectorDroneCircus>
        <ConnectionModeDroneCircus v-if="connectionModeSelectorShowing" @close="connectionModeSelectorShowing=false"></ConnectionModeDroneCircus>
        <DeviceModeDroneCircus v-if="deviceModeShowing" @close="deviceModeShowing=false"></DeviceModeDroneCircus>
    </div>    
</template>

<script>
import { defineComponent, ref, inject, onMounted, provide } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import InstructionsDroneCircus from './InstructionsDroneCircus.vue'
import ButtonsDroneCircus from './ButtonsDroneCircus.vue'
import MapDroneCircus from './MapDroneCircus.vue'
import DetectorDroneCircus from './DetectorDroneCircus.vue'
import LevelSelectorDroneCircus from './LevelSelectorDroneCircus.vue'
import ConnectionModeDroneCircus from './ConnectionModeDroneCircus.vue'
import DeviceModeDroneCircus from './DeviceModeDroneCircus.vue'
import mqtt, { MqttClient } from 'mqtt'

export default defineComponent({
    components: {
        InstructionsDroneCircus,
        ButtonsDroneCircus,
        MapDroneCircus,
        DetectorDroneCircus,
        LevelSelectorDroneCircus,
        ConnectionModeDroneCircus,
        DeviceModeDroneCircus
    },
    setup () {

        const route = useRoute()
        const router = useRouter()

        const emitter = inject('emitter');
        let client = inject('mqttClient');
        let clientAutopilot;

        let levelSelectorShowing = ref(false)
        let connectionModeSelectorShowing = ref(false)
        let deviceModeShowing = ref(true)

        let selectedLevel = ref("")
        let difficulty = ref("")
        let mode = ref("")  
        let connectionMode = ref("");

        let state = ref("idle");

        let mobileConnected = false; 

        emitter.on('selectedDeviceCircus', (data) => {
            if(data.device == 'mobile'){
                client.subscribe('mobileApp/droneCircusWebApp/#'); 
            }
        })
        
        emitter.on('selectedLevelCircus', (data) => {
            selectedLevel.value = data.level;                       
        })

        emitter.on('difficultyCircus', (data) => {
            difficulty.value = data.level;                      
        })

        emitter.on('selectedConnectionCircus', (data) => {
            connectionMode.value = data.mode;
            let external_broker_address;         
            if(connectionMode.value == "Global"){
                external_broker_address = "classpip.upc.edu"                
            }
            else if(connectionMode.value == "Local"){
                external_broker_address = "10.10.10.1"
            }
            let port = 8000;           
            createClient(external_broker_address, port);
        })
        
        emitter.on('directionCircus', (data) => {            
            if(state.value != "returning" && state.value != "practising" && !mobileConnected){
                if(data.direction == "Drop"){
                    clientAutopilot.publish('droneCircusWebApp/autopilotService/drop');
                    clientAutopilot.publish('droneCircusWebApp/autopilotService/reset');
                }
                else if(data.direction == "Return"){
                    returnHome();
                }
                else{
                    clientAutopilot.publish('droneCircusWebApp/autopilotService/go', data.direction);                
                }
            }
        })

        onMounted(() => {
            mode.value = route.params.mode;
            console.log(mode.value);
            client.publish("droneCircusWebApp/imageService/Connect","");            
            client.on('message', (topic,message) => {
                if(topic == 'mobileApp/droneCircusWebApp/connect'){
                    mobileConnected = true;                   
                    emitter.emit('mobileStateCircus', {'state': 'connected'})
                    client.publish('droneCircusWebApp/mobileApp/connected', mode.value)
                    console.log(mode.value)
                }
                else if(topic == 'mobileApp/droneCircusWebApp/finishPractice'){
                    emitter.emit('videoCaptureCircus', {'capturing':false, 'mobile': mobileConnected}); 
                    state.value = 'disconnected';
                    emitter.emit('finishPracticeCircus');
                }
                else if(topic == 'autopilotService/mobileApp/telemetryInfo'){
                    processMessage(message);
                }
                else if(topic == "mobileApp/autopilotService/returnToLaunch"){
                    state.value = 'returning'
                }
            })         
        })

        function showLevelSelector(){
            levelSelectorShowing.value = true;            
        }

        function practice(){
            state.value = "practising";
            let width = mobileConnected ? 300 : 400
            let height = mobileConnected ? 400 : 300
            
            const parameters = {
                mode: mode.value,
                level: difficulty.value,
                selected_level: selectedLevel.value,
                width: width,
                height: height
            }
            console.log(parameters)
            let message = JSON.stringify(parameters);
            client.publish("droneCircusWebApp/imageService/parameters", message);
            client.subscribe("imageService/droneCircusWebApp/videoFrame")
            client.subscribe("imageService/droneCircusWebApp/code")
            if(mobileConnected){
                client.publish("droneCircusWebApp/mobileApp/practice")
                //client.subscribe("imageService/mobileApp/videoFrame")
                client.subscribe("imageService/mobileApp/code")
                console.log('practice mobile started')
            } 
            emitter.emit('videoCaptureCircus',  {'capturing':true, 'state': state.value, 'mobile': mobileConnected}); 
                   
             
        }

        function selectConnectionMode(){
            if(!mobileConnected){
                connectionModeSelectorShowing.value = true;
            }
            else{
                client.subscribe("autopilotService/mobileApp/#");
                client.subscribe('mobileApp/autopilotService/returnToLaunch'); 
            }            
        }

        function createClient(external_broker_address, port){
            try{
                if(external_broker_address == 'localhost'){
                    clientAutopilot = mqtt.connect('mqtt://'+external_broker_address+':'+port) //proba a connectar-se
                }
                else if(external_broker_address == 'broker.hivemq.com'){
                    clientAutopilot = mqtt.connect('ws://'+external_broker_address+':'+port+'/mqtt') //proba a connectar-se
                }
                else if(external_broker_address == 'classpip.upc.edu'){
                    clientAutopilot = mqtt.connect('ws://'+external_broker_address+':'+port+'/mqtt', {
                        clean: false,
                        keepalive: 60,
                        clientId: "dashboardGames2",
                        connectTimeout: 4000,
                        username: 'dronsEETAC',
                        password: 'mimara1456.'
                    })
                }
                else{
                    clientAutopilot = mqtt.connect('mqtt://'+external_broker_address+':'+port)
                }                
                clientAutopilot.on('connect', () => { //si el commando que rep es 'connect', s'ha connectat bé
                    console.log("Connection autopilot succeeded!");
                })
                clientAutopilot.publish("droneCircusWebApp/autopilotService/connect");
                clientAutopilot.subscribe("autopilotService/droneCircusWebApp/#");

                clientAutopilot.on('message', (topic,message) => {
                    if(topic=="autopilotService/droneCircusWebApp/telemetryInfo"){
                        processMessage(message)
                    }                    
                })                
            }
            catch(error){
                console.log("mqtt.connect error ", error);
            }            
        }

        function arm(){
            if(mobileConnected){
                client.publish("mobileApp/autopilotService/armDrone")
            }
            else{
                clientAutopilot.publish("droneCircusWebApp/autopilotService/armDrone");
            }
        }

        function takeoff(){
            if(mobileConnected){
                client.publish("mobileApp/autopilotService/takeOff")
            }
            else{
                clientAutopilot.publish("droneCircusWebApp/autopilotService/takeOff");
            }            
        }

        function returnHome(){
            if(mobileConnected){
                client.publish("mobileApp/autopilotService/returnToLaunch")
            }
            else{
                clientAutopilot.publish("droneCircusWebApp/autopilotService/returnToLaunch");
            }             
        }

        function disconnect(){
            if(mobileConnected){
                client.publish("mobileApp/autopilotService/disconnect")
            }
            else{
                clientAutopilot.publish("droneCircusWebApp/autopilotService/disconnect");
            }            
        }

        function close(){
            if(state.value == 'connected'){                
                clientAutopilot.end()
            }            
            router.push('/mode');            
        }

        function stopPractice(){
            emitter.emit('videoCaptureCircus', {'capturing':false, 'mobile': mobileConnected}); 
            state.value = 'disconnected';            
            if(mobileConnected){
                emitter.emit('finishPracticeCircus')
                client.publish('droneCircusWebApp/mobileApp/finishPractice');
            }
           
        }

        function processMessage(message){     
                let telemetryInfo = JSON.parse(message);
                let stateAutopilot = telemetryInfo.state;
                let lat = telemetryInfo.lat;
                let long = telemetryInfo.lon;
                if (stateAutopilot == "connected" && state.value == "disconnected"){                            
                    state.value = "connected";
                    emitter.emit('autopilotStateCircus', {'state': state.value});
                    emitter.emit('autopilotPositionCircus',{'lat': lat, 'long': long});                                                  
                }
                else if(stateAutopilot == "armed" && state.value == "connected"){
                    console.log("armed");
                    state.value = "armed";
                    emitter.emit('autopilotStateCircus', {'state': state.value});
                }
                else if(stateAutopilot == "flying" && state.value != "flying"){
                    state.value = "flying";
                    emitter.emit('autopilotStateCircus', {'state': state.value})
                    emitter.emit('videoCaptureCircus',  {'capturing':true, 'state': state.value, 'mobile': mobileConnected});
                }
                else if(stateAutopilot == "flying" && state.value == "flying"){
                    emitter.emit('autopilotPositionCircus',{'lat': lat, 'long': long});  
                }
                else if(stateAutopilot == "returningHome" && state.value == "flying"){                            
                    state.value = "returning";
                    emitter.emit('autopilotPositionCircus',{'lat': lat, 'long': long});
                    emitter.emit('autopilotStateCircus', {'state': state.value});
                    emitter.emit('videoCaptureCircus',  {'capturing':false, 'state': state.value, 'mobile': mobileConnected});
                }
                else if(stateAutopilot == "returningHome" && state.value == "returning"){
                    emitter.emit('autopilotPositionCircus',{'lat': lat, 'long': long});
                    emitter.emit('autopilotStateCircus', {'state': state.value});
                }
                else if(stateAutopilot == "onHearth" && state.value == "returning"){
                    state.value = "onHearth";
                    emitter.emit('autopilotStateCircus', {'state': state.value});
                }
            
        }
        
        return {
            showLevelSelector,
            levelSelectorShowing,
            selectedLevel,
            difficulty,
            practice,
            selectConnectionMode,
            connectionModeSelectorShowing,
            deviceModeShowing,
            state,
            close,
            arm,
            takeoff,
            returnHome,
            disconnect,
            stopPractice
        }
    }
})
</script>

<style scoped>

</style>