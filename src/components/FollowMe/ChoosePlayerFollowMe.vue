<template>
    <div class="popup">
        <div class="popup-inner">
            <div class="row">
                <h2>What player will be in this point?</h2>
            </div> 
            <div v-for="(player, index) in props.players" :key="index" class="row">
                <b-button pill variant="outline-secondary" @click="select(player)">{{ player }}</b-button>
            </div>
            <div class="row">
                <b-button pill variant="danger" @click="close">Close</b-button>
            </div>                
        </div>
    </div>
</template>

<script>
import { defineComponent, inject, onMounted, ref } from 'vue'

export default defineComponent({
    props: {
        players: Array
    },

    setup (props, context) {

        const emitter = inject('emitter');
                
        function select(value){
            emitter.emit('playerChosenFollowMe', {'player':value}); // objecte json
            context.emit('close')
        }   

        function close(){
            context.emit('close')
        }

        return {
            select,
            props,
            close            
        }
    }
})
</script>

<style scoped>
.popup {
	position: fixed;
	top: 0;
	left: 0;
    padding-top: 10px; /* Location of the box */
    padding-bottom: 10px;

    width: 100%; /* Full width */
    height: 100%; /* Full height */

	z-index: 99;

    overflow: auto; /* Enable scroll if needed */

	background-color: rgba(0, 0, 0, 0.5);

    display: flex; 
	align-items: center;
	justify-content: center;
    
	
}
.popup-inner {
	background: white;
    width: 600px;
    height: 100%;
    display: flex; 
	align-items: center;
	justify-content: center;
    flex-direction: column;  
    border-radius: 10px;  
}

.row{
    background-color: white;
    padding-top: 10px;
    border-radius: 15px;
    width: 80%;
}

.button{
    width:100%;
    font-size: 20px;
    font-family:monospace;
    font-weight: bold;
    border: none;
    margin-top: 5%;
}
</style>