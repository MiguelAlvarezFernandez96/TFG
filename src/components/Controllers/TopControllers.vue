<template>

    <div class="topStyle">
        <h3 style="text-align: center; margin-top: 2%; margin-bottom: 2%;"> Connected players </h3>
        <div class="row" v-if="maxPlayersChosen" style="text-align: center; margin-top: 5%; margin-bottom: 2%;">
            <div class="col">
                <h5>{{ players[0] }}</h5>
            </div>
            <div class="col">
                <h5>{{ players[1] }}</h5>
            </div>
            <div class="col">
                <h5>{{ players[2] }}</h5>
            </div>
            <div class="col">
                <h5>{{ players[3] }}</h5>
            </div>
        </div>
        <div v-if="!maxPlayersChosen">
            <b-input-group prepend="How many players?" style="width:50%; margin-left: 22%; margin-top: 1%">
            <b-form-input placeholder="Max 4 players" v-model="maxPlayers"></b-form-input>
            <b-input-group-append>
                <b-button @click ="inputNumberPlayers" variant="info">Enter</b-button>
            </b-input-group-append>
            </b-input-group>
        </div>
    </div>


</template>

<script>
import { defineComponent, ref, inject, onMounted } from 'vue' // ref per les variables que canvien, inject per 
// https://www.npmjs.com/package/vue-sweetalert2
import Swal from 'sweetalert2'

export default defineComponent({
    components:{
    },
    setup () {
        let client = inject('mqttClient');
        const emitter = inject('emitter');
        let numPlayers = 0;
        let maxPlayers = ref(null);
        let players = ref([]);
        let maxPlayersChosen = ref(false);

        onMounted(() => {
            client.subscribe('mobileApp/dashboardControllers/username');

            client.on('message', (topic, message) => {
                if(topic=='mobileApp/dashboardControllers/username'){      
                    let success = InputUsername(message.toString());
                    let newTopic = 'dashboardControllers/mobileApp/'+message.toString()+'/create'
                    console.log(newTopic)                    
                    client.publish(newTopic, success);                    
                }
                else if(topic == "mobileApp/dashboardControllers/disconnect"){
                    players.value = [];
                    numPlayers = 0;
                    maxPlayers.value = null;   
                    maxPlayersChosen.value = false;                
                }
            })
        })
      
        function InputUsername(username){  
            let nameTaken = false;
            if(players.value.length < parseInt(maxPlayers.value)){
                for(var i = 0; i<players.value.length; i++){
                    if(username == players.value[i]){
                        nameTaken = true;
                    }
                }   
                if(!nameTaken){
                    players.value.push(username);
                    numPlayers = numPlayers + 1;
                    if(numPlayers == parseInt(maxPlayers.value)){
                        emitter.emit('playersControllers', {'players': players.value});          
                    }
                    return "ok"
                } 
                else{
                    return "error"
                }   
            }
            else{
                return "error"
            }              
        }

        function inputNumberPlayers(){
            
            if(parseInt(maxPlayers.value) <= 4 && parseInt(maxPlayers.value) >= 2){
                maxPlayersChosen.value = true;
            }
            else{
                Swal.fire("Write the number of players between 2 and 4");
            }
            
        }

        return {           
            InputUsername,  
            client,
            maxPlayers,
            players,
            maxPlayersChosen,
            inputNumberPlayers
        }
    }
})
</script>

<style scoped>
.topStyle{
    border-style: solid;
    border-color: rgb(0, 0, 0);
    border-radius: 20px;
    height: 22%;
    margin-bottom: 10px;
}
</style>