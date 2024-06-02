# Dashboard Games

## What is it?

Dashboard Games is a web app developed with Vue.js that host the dashboards for three different games aimed to be played with the Mobile App. These games allow an audience to participate and interact with the drone during an exhibition.

The games included are:
- **Drone Circus Game**: Allows to control the drone in different ways like using the poses of your body or your fingers to determine the direction. It is a remake of the Drone Circus desktop application and the feature of using the mobile as the camera is added.
- **Controllers Game**: It is a multiplayer game that allows each player to guide the drone from their mobile. To do this the dronelab is divided in sectors and each sector is assigned to a player. When the drone is in that sector, is the turn of the corresponding player to control it.
- **Follow Me Game**: In this game the players are distributed around the dronelab with their respectives mobiles. When it is the player's turn, they say a name of another player to the mobile and the drone moves to the position of that player and takes a photo of them. Then sends it to the rest of the players and it is the turn of the player of whom the picture has been taken.

## Installation

In order to run and contribute to the modules implemented in Vue, you need to install Node.js (version v16.13.0) and @vue/cli version 4.5.15. 
To contribute to must follow the contribution protocol describen in the main repo of the Drone Engineering Ecosystem. [![DroneEngineeringEcosystem Badge](https://img.shields.io/badge/DEE-MainRepo-brightgreen.svg)](https://github.com/dronsEETAC/DroneEngineeringEcosystemDEE) 
To run the application, after cloning the repo in your laptop you must execute these commands:

```
cd DashboardGames
npm install
npm run serve
```

## How to use it

To use this application within the Drone Engineering Ecosystem the global mode must be used. So first, make sure you have a broker with TLS configuration that you can access via MQTT. To change the parameters of the broker you must modify the main.ts file. You must also have the Autopilot Service running, on board if you are in production or on your computer if you are in simulation, in this last case make sure to have the internal broker running and the Mission Planner opened. Also, if you want to play the Drone Circus Game you must also have the Image Service running. 

As this application goes along with the Mobile App, you must have that app running and opened on some mobiles. Once the Dashboard Games is opened you can choose which game you want to play.

### Drone Circus Game

When you enter to this game a screen showing all the game modes is shown and you can choose. Note that only two of the four modes are fully implemented so you can only choose "Fingers" or "Poses". 

<img width="770" alt="Captura de pantalla 2023-07-26 124021" src="https://github.com/JoanaOP/DashboardGames/assets/73441184/f36441e8-e322-4f24-a215-c62b7d301f87">

Then you enter to the main page where you can choose the device from where to open the camera, the difficulty level and the scenario to play. If you choose the camera of the computer, it will start recording you so you can practice the movements you will do and see how the drone will move. 

<img width="833" alt="Captura de pantalla 2023-07-26 125122" src="https://github.com/JoanaOP/DashboardGames/assets/73441184/0bc8e493-f655-44ce-a468-1a4ec5dc0068">

If the device chosen is the mobile, a button indicating the state of the mobile appears, once the mobile is connected you will be able to start the practice.

When you are done with the practice you can stop it and connect to the Autopilot Service. Once connected you will be able to arm and take off the drone. From here it is your mission to guide the drone as you please and have fun. Once you are done, you can land the dron by clicking the "Return Home" button.

<img width="821" alt="Captura de pantalla 2023-07-26 125348" src="https://github.com/JoanaOP/DashboardGames/assets/73441184/f7882294-5b29-43b8-9c59-57688aa5a1cf">

### Demo
Have a look to the demo here: 
[Drone Circus demo](https://youtu.be/dd4ezG6JVHc)

### Controllers Game

After clicking this game the dashboard for the game is shown. In here you can see a top component to see the players connected and a map. First of all you must introduce the number of the players and wait until all of them are connected from their mobiles.

<img width="367" alt="Captura de pantalla 2023-08-17 131114" src="https://github.com/JoanaOP/DashboardGames/assets/73441184/1920e432-c1cc-4bca-9b4f-73defb735a5a">

Then you can choose two ways of assigning sectors to each player, choosing one of the predefined scenarios or creating you own scenario by drawing the sectors on the map. Once the sectors are defined, you can start the practice. In here, the movement of the drone is simulated so the players practice controlling the drone and planning what to do to reach the final base, which will be painted in pink.

<img width="357" alt="Captura de pantalla 2023-08-17 131145" src="https://github.com/JoanaOP/DashboardGames/assets/73441184/150de5b3-92a3-4de9-9561-a8cbc4887dc3">

Once the practice finishes, you can connect to the Autopilot Service and then arm and take off the drone. From here it will be the players responsability to reach the final base. If you want to land the drone, you can click the "Return Home" button.   

### Demo
Have a look to the demo here: 
[Controllers Game demo](https://youtu.be/AsAvQm1oCuE)

### Follow Me Game

When entering this game, the corresponding dashboard will be shown, which has a map, a list of connected players and some buttons. First of all, you must wait for the players to connect. 

When more than two players are connected you can start assigning positions for each one by clicking on the marks of the map. When all players are assigned a position, you can connect to the Autopilot Service and arm and take off the drone.

Then the game starts and it is the first player turn to say the name of another player. When the drone goes to that player and takes a photo, the photo will be displayed at the bottom of the dashboard. And the game will go on like this until the button "Return Home" is clicked.

<img width="481" alt="Captura de pantalla 2023-07-21 155804" src="https://github.com/JoanaOP/DashboardGames/assets/73441184/b48d55c4-ab9f-4c6f-a992-6615e7cd37a0">   

### Demo
Have a look to the demo here: 
[Follow Me demo](https://youtu.be/Bv_-wKKmF0E)

## Code
Have a look to the code here: 
[Dashboard Code](https://youtu.be/hAtsUjoCelU)



