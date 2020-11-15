<template>
<f7-page name="users">
    <f7-navbar back-link="Back">Flashy Cards</f7-navbar>
    
    <div>
        <div>
            <f7-block-title>Take a Picture of Your Notes</f7-block-title>
            <f7-block strong>
                <p>Ideally, take the picture with your phone alligned with the notes and with a good light source present.</p>
            </f7-block>
        </div>
        <div class = "camera-modal">
            <video ref="video" class="camera-stream"/>
        </div>
        
        <div style = "width:50%; margin: 0 auto;"><a @click="capture" class="button button-fill button-round button-small" href="#"><i class="material-icons ">camera</i></a> 
            </div>
    </div>
  </f7-page>
</template>

<script>
export default {
    data () {
      return {
        mediaStream: null
      }
    },
    mounted () {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((mediaStream) => {
          this.mediaStream = mediaStream
          this.$refs.video.srcObject = mediaStream
          this.$refs.video.play()
        })
        .catch(error => console.error('getUserMedia() error:', error))
    },
     methods: {
      capture () {
                const mediaStreamTrack = this.mediaStream.getVideoTracks()[0]
                const imageCapture = new window.ImageCapture(mediaStreamTrack)
                return imageCapture.takePhoto().then(blob => {
                    this.$root.img = blob;
                    console.log(blob)
                })
                
                const tracks = this.mediaStream.getTracks()
                tracks.map(track => track.stop())
      }
    },
    destroyed () {
        const tracks = this.mediaStream.getTracks()
        tracks.map(track => track.stop())
    }
  }
</script>
<style scoped>
    .camera-modal {
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: 10;
    }
    .camera-stream {
        width: 100%;
        max-height: 100%;
    }
</style>