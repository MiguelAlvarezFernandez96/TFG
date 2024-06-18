<template> 
    <h1 style="text-align: center">Dashboard for Controllers Game</h1>
    <div style="display:flex; margin-left:20%"> 
      <b-button :class="{ 'disabled-button': !CreatorModeActive }" style="width:40%; margin-left:2%; margin-top:5%" @click="ChangeMode('standard')" variant="info" size="lg" :disabled="!CreatorModeActive">Standard Mode</b-button>
      <b-button :class="{ 'disabled-button': CreatorModeActive }" style="width:40%; margin-left:2%; margin-top:5%" @click="ChangeMode('Creator')" variant="info" size="lg" :disabled="CreatorModeActive">Creator Mode</b-button>
</div>
    <div v-if = "mode=='standard'" :key="mode" class ="main">
      <TopControllers :mode="mode"></TopControllers>
      <div v-if = "ShowingScenarios==true" class ="main">
        <ScenariosControllers></ScenariosControllers>>
      </div>
      <MapsControllers :mode="mode"></MapsControllers>
    </div>
    <div v-if = "mode=='Creator'" :key="mode" class ="main">
      <TopControllersCreator :mode="mode"></TopControllersCreator>
      
      <MapsControllersCreator :mode="mode"></MapsControllersCreator>
    </div>

  </template>
  
  <script>
  import { onMounted, defineComponent, ref, inject } from 'vue';
  import MapsControllers from './MapsControllers.vue';
  import MapsControllersCreator from './MapsControllersCreator.vue';
  import TopControllers from './TopControllers.vue';
  import TopControllersCreator from './TopControllersCreator.vue';
  import ScenariosControllers from './ScenariosControllers.vue';
  import Swal from 'sweetalert2'
  
  export default defineComponent({
    components: {
      TopControllers,
      MapsControllers,
      ScenariosControllers,
      MapsControllersCreator,
      TopControllersCreator
    },
    setup () {  
      let CreatorModeActive = ref(false);
      let mode = ref('standard')
      function ChangeMode(newMode){
        mode.value= newMode;
        CreatorModeActive.value = !CreatorModeActive.value;
      }
      let ShowingScenarios = ref(false);
      function ShowScenarios(ShowEnable){
        ShowingScenarios.value = ShowEnable.value;
      }
      return {
        ChangeMode,
        mode,
        CreatorModeActive
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
    .disabled-button {
      background-color: grey !important; /* Cambia a tu color preferido */
      color: white; /* Si también quieres cambiar el color del texto */
    }
  
  </style>
  