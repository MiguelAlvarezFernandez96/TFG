<template>
    <div style="text-align: center; margin-bottom: 40px; margin-top: 20px;">
      <h2>Dashboard for Follow Me Game</h2>
    </div>    
    <div style="display:flex; justify-content: center;">
      <b-button v-if="!connected" :variant="connectColor" @click="connect" class="myButtonConnect">{{connectText}}</b-button>
      <b-button v-if="connected" variant="success" class="myButtonConnect">Connected</b-button>
      <b-button v-if="!flying" :variant="takeoffColor" @click="takeoff"  class="myButtonConnect" :disabled="!connected">{{ takeoffText }}</b-button>
      <b-button v-if="flying" variant="success"  class="myButtonConnect">Flying</b-button>
      <b-button v-if="!returning" variant="info" @click="rtl" :disabled="!flying" class="myButtonConnect">Return to Launch</b-button>
      <b-button v-if="returning" variant="success"  class="myButtonConnect">Returning...</b-button>
    </div>
    <div v-if="flying && !returning">
      <h2>Now following: {{ followingName }}</h2>
    </div>
    <div style="display: flex">
      <div style="width:80%; margin-left: 10px; margin-right: 5px;">
        <MapsFollowMe @canConnect="canConnect = true" @connected="connected = true" @flying="flying = true" @returning="returning = true" @onHearth="resetButtons()"></MapsFollowMe>
      </div>      
      <div style="width:20%; margin-left: 5px; margin-right: 10px; margin-top: 20px;">
        <table class="myTable">
          <tr>
            <th>
              Players:
            </th>
          </tr>
          <tr v-for="(name, index) in players" :key="index">
            <td>
              {{ name }}
            </td>
          </tr>
        </table>
      </div>      
    </div>
    <div style="display:flex; justify-content: center; margin-top: 10px;">
      <div  style ="width:70%; height:350px display: flex; justify-content: center;">
          <canvas style="width: 400px; height: 300px; border-style: solid;" id="output"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted, defineComponent, inject, ref } from 'vue';
  import Swal from 'sweetalert2'
  import MapsFollowMe from './MapsFollowMe'
  import * as cv from 'opencv.js'
  
  export default defineComponent({
    components: {
        MapsFollowMe
    },   

    setup (props, context) {
      const emitter = inject('emitter');
      let client = inject('mqttClient');
      let connected = ref(false);
      let flying = ref(false);
      let returning = ref(false);
      let canConnect = ref(false);

      let players = ref([])
      let followingName = ref("")

      let takeoffColor = ref("info");
      let connectColor = ref("info");
      let connectText = ref("Connect");
      let takeoffText = ref("Take off");



      onMounted (() => {

        client.subscribe("+/dashboardFollowme/#");

        emitter.on('followingFollowMe', (data) => {
          followingName.value = data
        })

        client.on('message', (topic, message) => {          

          if(topic=="mobileApp/dashboardFollowme/username"){
            let success = InputUsername(message.toString());
            let newTopic = 'dashboardFollowme/mobileApp/'+message.toString()+'/create';                   
            client.publish(newTopic, success);            
          }

          else if(topic=="mobileApp/dashboardFollowme/sendList"){
            console.log(players.value)
            client.publish('dashboardFollowme/mobileApp/updateList', JSON.stringify({players: players.value}))            
          }

          else if(topic == "cameraService/dashboardFollowme/picture"){
            const img = new Image();
            img.src = "data:image/jpg;base64,"+message;
            img.onload = () => {        
              let dst = cv.imread(img);
              cv.imshow ('output',dst);
              console.log('picture')
            }
          }       


        })
      })

      function connect(){
          if(connected.value == false){
            if(players.value.length < 2){              
              Swal.fire("There must be at least 2 players to start")
            }
            else{
              if(canConnect.value){
                client.publish('dashboardFollowme/autopilotService/connect','');
                connectColor.value = "warning"
                connectText.value = "Connecting..."
              }
              else{
                Swal.fire("Assign a position to players by clicking the markers")
              }
            } 
          }
          else if(connected.value == true && flying.value == false && returning.value == false){
            client.publish('dashboardFollowme/autopilotService/disconnect');
            connectColor.value = "info"
            connectText.value = "Connect"
            connected.value = false;
          }
          else{
            Swal.fire("You can not disconnect if you are flying")
          }    
               
      }
  
      function takeoff(){
        client.publish('dashboardFollowme/autopilotService/armAndTakeoff');
        takeoffColor.value = "warning"
        takeoffText.value = "Taking off..."
      }  
      
      function rtl(){
        client.publish('dashboardFollowme/autopilotService/returnToLaunch')
      }

      function resetButtons(){
        connected.value = true;
        flying.value = false;
        returning.value = false;
        takeoffColor.value = "info";
        takeoffText.value = "Take off"
      }

      function InputUsername(username){  
        let nameTaken = false;
        for(var i = 0; i<players.value.length; i++){
          if(username == players.value[i]){
            nameTaken = true;
          }
        }   
        if(!nameTaken){
          players.value.push(username);
          emitter.emit('newPlayerFollowMe',username);
          return "ok"
        } 
        else{
          return "error"
        }   
      }

      
  
      return {
        connect,
        takeoff,
        rtl,
        players,
        resetButtons,
        connected,
        flying,
        returning,
        followingName,
        takeoffColor,
        takeoffText,
        connectColor,
        connectText,
        canConnect
      }
    }
  });
  </script>
  
  <style>
    .main {
      height: 1000px;    
      margin-left: 5px;
      margin-right: 5px;
    }
    .myButtonConnect {
      margin-left: 5%; 
      margin-right: 5%; 
      margin-bottom: 5px; 
      width:70%;
      height: 50px;
    }
    .myTable {
      border-collapse: collapse;
      border: 1px solid;
      width: 100%
    }

    th, td {
      padding-left: 15px;
      padding-top: 10px;
      padding-bottom: 10px;
      text-align: left;
    }

    th {
      background-color: #59c1d3;
      color: black;
    }

    tr:nth-child(even) {background-color: #f2f2f2;}
  
  </style>
  