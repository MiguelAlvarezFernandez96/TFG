<template>
    <div class="popup">
        <div class="popup-inner">
            <div>
                <video style="width: 600px; height: 350px;;" autoplay >
                    <source src="../../assets/DroneCircusAssets/terraDeDrons.mp4">
                </video>
            </div>
            <b-button @click="close" variant="danger" style="width:50%; font-size: 15px; font-family:monospace; font-weight: bold; ">Close</b-button>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    setup (props, context) {
        
        function close(){
            context.emit('close'); // el context es passa com a parametre del setup
        }

        return {
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
    width: 650px;
    height: 450px;
    display: flex; 
	align-items: center;
	justify-content: center;
    flex-direction: column;
    border-radius: 5%;

}
</style>
