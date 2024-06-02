<template>    
    <div class="leftStyle">        
        <div style="display:flex; justify-content: center;">
            <div  style ="width:70%; height:350px display: flex; justify-content: center;">
                <canvas ref="canvasOut" style="width: 400px; height: 300px; border-style: solid;" id="output"></canvas>
                <!-- <img style="width: 400px; height: 300px; border-style: solid;" :src="imageList[indexToShow]" > -->
            </div>
       </div>
    </div>
    <div style="background-color: blue;">
        <video ref="video" @canplay="initCanvas()" style="display:none"></video>
        <canvas ref="canvas" style="display:none"></canvas>
    </div>
</template>

<script>
import { defineComponent, inject, ref } from 'vue'
import * as cv from 'opencv.js'

export default defineComponent({
    mounted(){
        this.video = this.$refs.video
        this.canvas = this.$refs.canvas
        this.canvasOut = this.$refs.canvasOut.getContext('2d');
        this.direction = 'Stop'
        this.mode = this.$route.params.mode;

        this.emitter.on('videoCaptureCircus', (cap) => {
            if(cap.capturing && !cap.mobile){                
                this.startCapture();
            }
            else if(!cap.capturing && !cap.mobile){
                this.stopCapture();
            }
        })

        this.emitter.on('directionCircus', (data) => {
            this.direction = data.direction;
        })

        this.client.on('message', (topic,message) =>{
            if(topic == "imageService/droneCircusWebApp/videoFrame"){
                let data = JSON.parse(message);
                let landmarksJSON = data.landmarks;
                this.indexToShow = parseInt(data.index);  
                this.showImage(this.indexToShow, landmarksJSON);              
            }
        })

    },
    methods:{
        startCapture() {            
            navigator.mediaDevices.getUserMedia({ video: true, audio: false}).then(stream => {
                if(this.video){
                    this.stream = stream;
                    this.video.srcObject = this.stream;
                    this.video.play()
                }               
                
            }).catch(error => {
                console.log(error);
            })
        },
        initCanvas(){
            this.canvas.setAttribute('width', 400)
            this.canvas.setAttribute('height', 300)
            let index = 0;
            this.interval = setInterval(() => {
                let context = this.canvas.getContext('2d');
                context.drawImage(this.video, 0,0, 400, 300);
                let jpg_as_text = this.canvas.toDataURL("image/jpeg").split(';base64,')[1];                 
                let data = {
                    "image": jpg_as_text,
                    "index": index
                }
                index = index + 1;
                let dataJSON = JSON.stringify(data);
                this.client.publish("droneCircusWebApp/imageService/videoFrame",dataJSON);
                this.imageList.push(this.canvas.toDataURL("image/jpeg"));                
            }, 400);
        },
        stopCapture(){
            this.stream.getTracks().forEach(function(track) {
                track.stop();
            });
            clearInterval(this.interval);            
            this.client.publish("droneCircusWebApp/imageService/stopVideoStream");
            this.imageList = [];            
        },
        
        showImage(index, landmarksJSON) {   
            const img = new Image();        
            img.src = this.imageList[index];
            console.log(this.imageList.length);
            console.log(this.indexToShow);
            img.onload = () => {                               
                let dst;
                dst = cv.imread (img);
                cv.imshow ('output',dst);
                this.canvasOut.font = "bold 50px Arial";
                this.canvasOut.fillStyle = "red";
                this.canvasOut.textBaseline = "bottom";
                this.canvasOut.fillText(this.direction, 50, 80);
                this.paintLandmarks(landmarksJSON);
            }
        },
        
        paintLandmarks(landmarksJSON){
            if(this.mode == "fingers"){
                landmarksJSON.forEach((hand) => {
                    if(hand.length > 0){
                        // thumb
                        for(let i = 0; i < 4; i++){
                            this.drawLine(400-hand[i].x*400, hand[i].y*300, 400-hand[i+1].x*400, hand[i+1].y*300);
                        }
                        // index
                        this.drawLine(400-hand[0].x*400, hand[0].y*300, 400-hand[5].x*400, hand[5].y*300);
                        for(let i = 5; i<8; i++){
                            this.drawLine(400-hand[i].x*400, hand[i].y*300, 400-hand[i+1].x*400, hand[i+1].y*300);
                        }
                        // middle
                        this.drawLine(400-hand[5].x*400, hand[5].y*300, 400-hand[9].x*400, hand[9].y*300)
                        for(let i = 9; i<12; i++){
                            this.drawLine(400-hand[i].x*400, hand[i].y*300, 400-hand[i+1].x*400, hand[i+1].y*300);
                        }
                        // ring
                        this.drawLine(400-hand[9].x*400, hand[9].y*300, 400-hand[13].x*400, hand[13].y*300)
                        for(let i = 13; i<16; i++){
                            this.drawLine(400-hand[i].x*400, hand[i].y*300, 400-hand[i+1].x*400, hand[i+1].y*300);
                        }
                        // pinky
                        this.drawLine(400-hand[13].x*400, hand[13].y*300, 400-hand[17].x*400, hand[17].y*300)
                        this.drawLine(400-hand[0].x*400, hand[0].y*300, 400-hand[17].x*400, hand[17].y*300)
                        for(let i = 17; i<20; i++){
                            this.drawLine(400-hand[i].x*400, hand[i].y*300, 400-hand[i+1].x*400, hand[i+1].y*300);
                        }
                    }
                    for(let i = 0; i<hand.length; i++){
                        this.drawCircle(400-hand[i].x*400, hand[i].y*300);
                    }       
                })
            }
            else if(this.mode == "pose"){
                if(landmarksJSON.length > 0){
                    // trunk
                    this.drawLine(400-landmarksJSON[11].x*400, landmarksJSON[11].y*300, 400-landmarksJSON[12].x*400, landmarksJSON[12].y*300);
                    this.drawLine(400-landmarksJSON[11].x*400, landmarksJSON[11].y*300, 400-landmarksJSON[23].x*400, landmarksJSON[23].y*300);
                    this.drawLine(400-landmarksJSON[12].x*400, landmarksJSON[12].y*300, 400-landmarksJSON[24].x*400, landmarksJSON[24].y*300);
                    this.drawLine(400-landmarksJSON[23].x*400, landmarksJSON[23].y*300, 400-landmarksJSON[24].x*400, landmarksJSON[24].y*300);
                    // right arm
                    for(let i = 11; i < 19; i = i + 2){
                        this.drawLine(400-landmarksJSON[i].x*400, landmarksJSON[i].y*300, 400-landmarksJSON[i+2].x*400, landmarksJSON[i+2].y*300);
                    }
                    this.drawLine(400-landmarksJSON[15].x*400, landmarksJSON[15].y*300, 400-landmarksJSON[21].x*400, landmarksJSON[21].y*300);
                    // left arm
                    for(let i = 12; i < 20; i = i + 2){
                        this.drawLine(400-landmarksJSON[i].x*400, landmarksJSON[i].y*300, 400-landmarksJSON[i+2].x*400, landmarksJSON[i+2].y*300);
                    }
                    this.drawLine(400-landmarksJSON[16].x*400, landmarksJSON[16].y*300, 400-landmarksJSON[22].x*400, landmarksJSON[22].y*300);
                    // left leg
                    for(let i = 24; i < 32; i = i + 2){
                        this.drawLine(400-landmarksJSON[i].x*400, landmarksJSON[i].y*300, 400-landmarksJSON[i+2].x*400, landmarksJSON[i+2].y*300);
                    }
                    this.drawLine(400-landmarksJSON[28].x*400, landmarksJSON[28].y*300, 400-landmarksJSON[32].x*400, landmarksJSON[32].y*300);
                    // right leg
                    for(let i = 23; i < 31; i = i + 2){
                        this.drawLine(400-landmarksJSON[i].x*400, landmarksJSON[i].y*300, 400-landmarksJSON[i+2].x*400, landmarksJSON[i+2].y*300);
                    }
                    this.drawLine(400-landmarksJSON[27].x*400, landmarksJSON[27].y*300, 400-landmarksJSON[31].x*400, landmarksJSON[31].y*300);
                }
                

                for(let i = 11; i<landmarksJSON.length; i++){
                    this.drawCircle(400-landmarksJSON[i].x*400, landmarksJSON[i].y*300);
                }  
            }
            
        },

        drawCircle(posx, posy){
            this.canvasOut.fillStyle = "#FF0000";
            this.canvasOut.beginPath();
            this.canvasOut.arc(posx, posy, 3, 0, 2 * Math.PI);
            this.canvasOut.fill();
        },

        drawLine(posx, posy, posx2, posy2){
            this.canvasOut.beginPath();
            this.canvasOut.moveTo(posx, posy);
            this.canvasOut.lineTo(posx2, posy2);
            this.canvasOut.lineWidth = 3;
            this.canvasOut.strokeStyle = "#FFFFFF";
            this.canvasOut.stroke();
        }
        
    },
    data() {        
        return{
            video: null,
            canvas: null,
            capturing: false,
            stream: null,
            interval: null,
            imageList: [],
            indexToShow: 0,
            direction: null,
            mode: null           
        }
    }, 

    setup () {

        let client = inject('mqttClient');
        let emitter = inject('emitter');     

        return {
            client,
            emitter
        }
    }
})
</script>

<style scoped>

.leftStyle{
        width: 100%;
    }

</style>