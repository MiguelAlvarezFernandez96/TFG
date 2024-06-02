<template>
    <div>
        <img v-bind:src="modeUrl">
    </div>
</template>

<script>
import { defineComponent, ref, onMounted, inject } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent({    
    setup () {
        const route = useRoute()
        let modeUrl = ref("")
        let difficulty = ref("")
        let mode = ref("")

        onMounted(() => {
            mode.value = route.params.mode;
        })

        const emitter = inject('emitter');

        emitter.on ('difficultyCircus', (data) => {
            difficulty.value = data.level;

            if(mode.value == "fingers"){
                modeUrl.value = require("../../assets/DroneCircusAssets/dedos_faciles.png")                               
            }
            else if(mode.value == "faces"){                
                modeUrl.value = require("../../assets/DroneCircusAssets/caras_faciles.png")
            }
            else if(mode.value == "pose"){
                console.log(difficulty.value)
                if(difficulty.value == "easy"){
                    console.log('easy')
                    modeUrl.value = require("../../assets/DroneCircusAssets/poses_faciles.png")
                }
                else if(difficulty.value == "difficult"){
                    modeUrl.value = require("../../assets/DroneCircusAssets/poses_dificiles.png")
                }
            }
            else{
                if(difficulty.value == "easy"){
                    modeUrl.value = require("../../assets/DroneCircusAssets/voces_faciles.png")
                }
                else if(difficulty.value == "difficult"){
                    modeUrl.value = require("../../assets/DroneCircusAssets/voces_dificiles.png")
                }                
            }                      
        })

        return {
            modeUrl,
            difficulty
        }
    }
})
</script>

<style scoped>
    img {
        max-width: 100%;
        max-height: 100%;
    }
</style>