<template>
    <div class="popup">
        <div class="popup-inner">
            <div class="row">
                <div class="col" style="text-align: center;"> 
                    <div style="height:450px">
                        <img src="../../assets/DroneCircusAssets/globalMode.png" style="width:100%; border-radius: 10px;">
                    </div>                    
                    <b-button @click="select('Global')" class="button">Global Mode</b-button>
                </div>
                <div class="col"> 
                    <div style="height:450px"> 
                        <img src="../../assets/DroneCircusAssets/localMode.png" style="width:100%; border-radius: 10px;">
                    </div>                    
                    <b-button @click="select('Local')" class="button">Local Mode</b-button>
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
            emitter.emit('selectedConnectionCircus', {'mode':value}); // objecte json
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
	background: rgba(0, 0, 0, 0);
    width: 1200px;
    height: 800px;
    display: flex; 
	align-items: center;
	justify-content: center;
    flex-direction: column;    
}

.row{
    background-color: #EDF4F2;
    padding-top: 10px;
    border-radius: 15px;
    height: 550px;
}

.button-backround{
    background-color: #EDF4F2;
    padding-top: 10px;
}
.button{
    width:100%;
    font-size: 20px;
    font-family:monospace;
    font-weight: bold;
    background-color: #973a93;
    color: #f1f437;
    border: none;
    margin-top: 10px;
}
</style>