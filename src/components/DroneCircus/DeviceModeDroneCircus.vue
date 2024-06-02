<template>
    <div class="popup">
        <div class="popup-inner">
            <div class="row" style="margin-top: 2%;">
                <h2>In which device do you want to play?</h2>
            </div>
            <div class="row" style="margin-bottom: 2%;">
                <div class="col" style="text-align: center;"> 
                    <img src="../../assets/DroneCircusAssets/mobile.png" style="width:60%; border-radius: 10px; margin-bottom: 2%;">
                    <b-button @click="select('mobile')" class="button">Mobile</b-button>
                </div>
                <div class="col"> 
                    <img src="../../assets/DroneCircusAssets/computer.png" style="width:60%; border-radius: 10px; margin-bottom: 2%;">
                    <b-button @click="select('computer')" class="button">Computer</b-button>
                </div>
            </div>                       
        </div>
    </div>
</template>

<script>
import { defineComponent, inject } from 'vue'

export default defineComponent({
    setup (props, context) {

        const emitter = inject('emitter');

        function select(value){
            emitter.emit('selectedDeviceCircus', {'device':value}); // objecte json
            context.emit('close')
        }
        return {
            select
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
	background: #EDF4F2;
    width: 800px;
    height: 400px;
    display: flex; 
	align-items: center;
	justify-content: center;
    flex-direction: column;  
    border-radius: 15px;  
}

.row{
    padding-top: 10px;
    height: 370px;
}

.button-backround{
    background-color: #EDF4F2;
    padding-top: 10px;
}
.button{
    width:80%;
    font-size: 20px;
    font-family:monospace;
    font-weight: bold;
    background-color: #973a93;
    color: #f1f437;
    border: none;
    margin-top: 10px;
}
</style>