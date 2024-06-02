<template>
    <div class="container mt-4" :style="{ marginBottom: dynamicMarginBottom }">
        <div class="container">
            <div class="row" v-if="numPlayers === 4">
              <div class="d-flex flex-wrap">
                <div
                  class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 mb-4"
                  v-for="(scenario, index) in props.scenario2vector"
                  :key="index"
                  style="flex: 0 0 20%; max-width: 20%;"
                >
                  <img :src="scenario" class="img-fluid img-thumbnail" />
                  <b-button @click="select(index)" class="button w-100 mt-2">Scenario</b-button>
                </div>
              </div>
            </div>
          </div>   
            <div class="container">
                <div class="row" v-if="numPlayers === 3">
                  <div class="d-flex flex-wrap">
                    <div
                      class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 mb-4"
                      v-for="(scenario, index) in props.scenario2vector"
                      :key="index"
                      style="flex: 0 0 20%; max-width: 20%;"
                    >
                      <img :src="scenario" class="img-fluid img-thumbnail" />
                      <b-button @click="select(index)" class="button w-100 mt-2">Scenario</b-button>
                    </div>
                  </div>
                </div>
              </div>   
            <div class="container">
                <div class="row" v-if="numPlayers === 2">
                  <div class="d-flex flex-wrap">
                    <div
                      class="col-12 col-sm-6 col-md-4 col-lg-3 col-xl-2 mb-4"
                      v-for="(scenario, index) in props.scenario2vector"
                      :key="index"
                      style="flex: 0 0 20%; max-width: 20%;"
                    >
                      <img :src="scenario" class="img-fluid img-thumbnail" />
                      <b-button @click="select(index)" class="button w-100 mt-2">Scenario</b-button>
                    </div>
                  </div>
                </div>
              </div>   
            </div>            
</template>

<script>
import { defineComponent, inject, onMounted, ref } from 'vue'

export default defineComponent({

    props: {
        numPlayers: Number,
        scenario2vector: Array,
    },
    computed: {
    dynamicMarginBottom() {
      const numLines = Math.floor(this.scenario2vector.length / 5); // Número de líneas truncado
      const dynamicMargin = 5 + (10 * numLines); // Cálculo del margen inferior
      return `${dynamicMargin}%`; // Formateo del margen como cadena CSS
    }
  },
    setup (props, context) {
        
        const emitter = inject('emitter');
        function select(value){
            emitter.emit('scenarioSelectedControllers', {'scenario':value}); // objecte json
            context.emit('close');
            console.log ('Hola');
            console.log (props.scenario2vector[value]);
        }   
        

        return {
            select,
            props
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
    height: 500px;
    display: flex; 
	align-items: center;
	justify-content: center;
    flex-direction: column;    
}

.row{
    background-color: #EDF4F2;
    padding-top: 10px;
    border-radius: 15px;
    height: 370px;
    flex-wrap: wrap;
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
.img-fluid {
    width: 100%;
    height: auto;
    border-radius: 10px;
  }
  .img-thumbnail {
    max-height: 200px; /* Ajusta esto según tus necesidades */
  }
  .mt-4 {
    margin-top: 2%;
  }
  .mb-4 {
    margin-bottom: 2%;
  }
  .container {
    margin-bottom: 15%;
  }
</style>