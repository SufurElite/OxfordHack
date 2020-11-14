<template>
  <f7-page name="cards" theme-dark>
    <f7-navbar :sliding="false" large>
      <div>
        <f7-button class = "button-fill button-round" v-on:click="onLogoutClicked" style="text-align:left; width:100%"> Logout </f7-button>
        <f7-button v-on:click="onLogoutClicked" style="text-align:left; width:100%"> About </f7-button>
      </div>
      <h4 style="text-align:right; width: 100%;">{{this.email}}</h4>
      <f7-nav-title-large sliding style="text-align:center; width: 100%;">RevAIse</f7-nav-title-large>
    </f7-navbar>
    <f7-list class = "smart-select">
      <f7-list-item title="Study Set"> 
        <select v-model="Flashset">
          <option v-for="set in FlashSets" :key="set.fileID"> <p class = "text-align-center" style="font-size:large"> {{ set.setname }} </p> </option>
        </select>
      </f7-list-item>
    </f7-list>
    <!-- Tabbar for switching views-tabs -->
    <f7-toolbar tabbar labels bottom>
      <f7-link link="#" tab-link-active icon-md="material:note" text="Cards"></f7-link>
      <f7-link @click="toScan"  icon-md="material:camera_alt" text="Scan"></f7-link>
    </f7-toolbar>
  </f7-page>
</template>


<script>
import routes from '../js/routes.js';
import firebase from 'firebase';
import { db } from '../js/app';
import { firebaseApp } from '../js/app';
import dropdown from 'vue-dropdowns'
import 'firebase/auth';

export default {
  data() {
      return {
        email: firebase.auth().currentUser.email,  
        FlashSets: [],
        Flashset: '',
        object: {
          name: 'Flashcard Sets',
        },
      };
    },
    mounted() {
    db.collection('flashcards').where('email','==',this.email).get().then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        this.FlashSets.push(doc.data());
      });
    });
  },
  components: {
            'dropdown': dropdown,
  },
  methods: {
      onLogoutClicked() {
        firebase.auth().signOut().catch((error) =>{
          console.error("Error when trying to logout user", error);
        });  
        this.$f7.views.main.router.navigate('/');
      },
      toScan(){
        this.$f7.views.main.router.navigate('/home/');
      },
      selectMethod(payload){
        this.object.name = payload.setname;
      },
  }

}
</script>