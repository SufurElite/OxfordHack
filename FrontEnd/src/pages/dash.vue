<template>
  <f7-page name="home" theme-dark>
    <f7-navbar :sliding="false" large>
      <div>
        <f7-button class = "button-fill button-round" v-on:click="onLogoutClicked" style="text-align:left; width:100%"> Logout </f7-button>
        <f7-button v-on:click="onLogoutClicked" style="text-align:left; width:100%"> About </f7-button>
      </div>
      <h4 style="text-align:right; width: 100%;"> {{this.email}}</h4>
      <f7-nav-title-large sliding style="text-align:center; width: 100%;">Create a Study Set</f7-nav-title-large>
    </f7-navbar>
    
    <form @submit.prevent="addFlashcardSet(flashSetName)" action="" method="GET">
      <f7-list >
        <f7-list-input large class="username-input" :value="flashSetName" @input="flashSetName = $event.target.value" placeholder="Flashcard Set Name" />
      </f7-list>
      <f7-list class = "smart-select">
      <f7-list-item title="Subject"> 
        <select v-model="Subject">
          <option value="History">History</option>
          <option value="English">English</option>
          <option value="Mathematics">Mathematics</option>
          <option value="Language">Language</option>
          <option value="Science">Science</option>
        </select>
      </f7-list-item>
    </f7-list>
    <f7-row>
      <f7-col>
        <f7-button class = "button button-fill button-round" href="/camera/"> Take a Picture </f7-button>
      </f7-col>
      <f7-col>
        <input type="file" ref="file" @change="saveFile" style="display: none">
        <f7-button class = "button button-fill button-round" @click="$refs.file.click()"> Upload a File </f7-button>
      </f7-col>
    </f7-row>
      <f7-button class = "button button-fill button-round color-gray" type ="submit"> Add New Set </f7-button>
    </form>  
    

    
    <!-- Tabbar for switching views-tabs -->
    <f7-toolbar tabbar labels bottom>
      <f7-link @click="toCards" icon-md="material:note" text="Cards"></f7-link>
      <f7-link link="#" tab-link-active icon-md="material:camera_alt" text="Scan"></f7-link>
    </f7-toolbar>
  </f7-page>
</template>

<script>
import routes from '../js/routes.js';
import firebase from 'firebase';
import { db } from '../js/app'
import { storage } from '../js/app'
import 'firebase/auth';
import axios from 'axios'

export default {
  
  data() {
      return {
        email: firebase.auth().currentUser.email,
        flashSetName: '',
        Subject: '',
        isImage: null,
        File: null
      };
    },
  methods: {
      onLogoutClicked() {
        firebase.auth().signOut().catch((error) =>{
          console.error("Error when trying to logout user", error);
        });  
        this.$f7.views.main.router.navigate('/');
      },
      toCards(){
        this.$f7.views.main.router.navigate('/cards/');
      },
      selectMethod(payload){
        this.subject.name = payload.username;
      },
      saveFile(event){
      this.File = event.target.files[0];
      console.log(this.File)
      var type = event.target.files[0]['type'];
      console.log(type);
      if(type=="image/jpeg" || type=="image/png" || type == "image/gif"){
        this.isImage = true;
      } else { 
        this.isImage = false;
      }
      },
      addFlashcardSet(flashSetName) {
          if((this.flashSetName=='' || this.Subject=='') || (this.$root.img == null && this.File == null)){
              this.$f7.dialog.alert('Please fill out all the information first.');
          } else{
            if(this.isImage || this.File == null){
              var m = Math.random();
              var dest = 'images/picture-'+this.Subject+this.flashSetName+m.toString();
              if (this.File == null){
                var upload = this.$root.img;
              } else{
                var upload = this.File;
              }
            } else { 
              var m = Math.random();
              var dest = 'Files/file-'+this.Subject+this.flashSetName+m.toString();
              var upload = this.File;
            }
            storage.ref().child(dest).put(upload).then(res => { console.log(res) })
            
            var res = {"setname" : this.flashSetName, "subject" : this.Subject, "email": this.email, "fileID":dest}
            console.log(res);
            db.collection('flashcards').add(res)
            //https://cors-anywhere.herokuapp.com/https://revaise.ew.r.appspot.com
            axios.post('http://127.0.0.1:5000/parse/', {
              setname: this.flashSetName,
              subject: this.Subject,
              email: this.email, 
              fileID: dest
            }).then((response)=>{
              console.log(response.data);  
              this.$root.img = null;
              this.File = null;
              this.isImage = null;
            })
          }
      },
  }
}
</script>