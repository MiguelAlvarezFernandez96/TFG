<template>
    <div style="display: flex; justify-content: center; flex-direction: column; background-color: #EEEEEE;">
        <div style="text-align: center; ">
            <img src="../../assets/DroneCircusAssets/gallery.png" style="width:100%">
        </div>
        <div class="row" >
            <div class="col" style="text-align: center;">
                <router-link to="/main/voice" custom v-slot="{ navigate }">
                    <b-button @click="navigate" role="link" class="button">Voice</b-button>
                </router-link>             
            </div>
            <div class="col" style="text-align: center;">
                <router-link to="/main/pose" custom v-slot="{ navigate }">
                    <b-button @click="navigate" role="link" class="button">Pose</b-button>
                </router-link>             
            </div>
            <div class="col" style="text-align: center;">
                <router-link to="/main/fingers" custom v-slot="{ navigate }">
                    <b-button @click="navigate" role="link" class="button">Fingers</b-button>
                </router-link>             
            </div>
            <div class="col" style="text-align: center;">
                <router-link to="/main/faces" custom v-slot="{ navigate }">
                    <b-button @click="navigate" role="link" class="button">Faces</b-button>
                </router-link>                
            </div>            
        </div>
        <div class="row" style="padding-top: 30px;">
            <div class="col" style="text-align: center;">
                <router-link to="/" custom v-slot="{ navigate }">
                    <b-button @click="navigate" role="link" variant="danger" style="width:20%; font-size: 20px; font-family:monospace; font-weight: bold; background-color: #DD2915; color: #EEEEEE;">Exit</b-button>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
    setup () {
        
        return {}
    }
})
</script>

<style scoped>
.button{
    width:95%;
    font-size: 30px;
    font-family:monospace;
    font-weight: bold;
    background-color: #973a93;
    color: #f1f437;
    border: none;
}
</style>