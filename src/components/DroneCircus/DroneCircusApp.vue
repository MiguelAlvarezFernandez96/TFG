<template>
    <div style="display: flex; justify-content: center;">
        <div class="background">
            <div class="buttonColumn">
                <div style="text-align: center; margin-top: 350px;"> 
                    <router-link to="/mode" custom v-slot="{ navigate }">
                        <b-button @click="navigate" role="link" variant="success" style="width:90%; font-size: 40px; font-family:monospace; font-weight: bold; ">Enter</b-button>
                    </router-link>
                </div>
                <div style="text-align: center; margin-top: 50px">
                    <b-button @click="showVideo" variant="danger" style="width:90%; font-size: 20px; font-family:monospace; font-weight: bold; ">Sponsored by...</b-button>
                </div>
                <VideoDroneCircus v-if="showVideoPopUp" @close="closeVideo"></VideoDroneCircus>
            </div>
        </div>
    </div>
    
</template>

<script>
import { defineComponent, ref } from 'vue'
import VideoDroneCircus from './VideoDroneCircus.vue'

export default defineComponent({
    components: {
        VideoDroneCircus
    },
    setup () { 

        let showVideoPopUp = ref(false)

        function showVideo(){
            showVideoPopUp.value = true;
        }

        function closeVideo(){
            showVideoPopUp.value = false;
        }

        return {
            showVideoPopUp,
            showVideo,
            closeVideo
        }
    }
})
</script>

<style>
    .background{
        background-image: url("../../assets/DroneCircusAssets/entrada.png");
        background-color: #EEEEEE;
        height: 900px;
        width: 1300px;
        background-size: 1300px;
        display: flex;
        justify-content: center;
    }
    .buttonColumn {
        display: flex;
        justify-content: center;
        flex-direction: column;
        width: 20%;
    }
    
</style>