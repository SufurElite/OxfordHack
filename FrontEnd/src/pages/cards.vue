<template>
  <f7-page name="cards" theme-dark>
    <f7-navbar :sliding="false" large>
      <div>
        <f7-button class = "button-fill button-round" v-on:click="onLogoutClicked" style="text-align:left; width:100%"> Logout </f7-button>
        <f7-button v-on:click="toAbout" style="text-align:left; width:100%"> About </f7-button>
      </div>
      <h4 style="text-align:right; width: 100%;">{{this.email}}</h4>
      <f7-nav-title-large sliding style="text-align:center; width: 100%;">Flashy Cards</f7-nav-title-large>
    </f7-navbar>
    <f7-list class = "smart-select">
      <f7-list-item title="Study Set"> 
        <select v-model="Flashset" @change="loadCards">
          <option v-for="set in FlashSets" :key="set.name"> <p class = "text-align-center" style="font-size:large"> {{ set.name }} </p> </option>
        </select>
      </f7-list-item>
    </f7-list>


    <!--Flash card template : 
    Using edited version https://codepen.io/mgnmrt/pen/pKZVYg
     -->
    <div id="flashCardApp" class="container flex-grid-thirds">
    <div v-for="card in loadedCards" v-bind:key="card.id" v-bind:class="card.color" class="card card-front">
            <transition name="flip">
                <div v-show="!card.flipped" @click="flipCard(card)" class="card-text card-front-text">
                    <h2>
                        {{card.question}}
                    </h2>

                    <button class="button-white button-clear button-large">
                        FLIP
                        <i class="fas fa-sync-alt"></i>
                    </button>
                </div>
            </transition>

            <transition name="flip">
                <div v-show="card.flipped" @click="flipCard(card)" class="card-text card-back-text">
                    <h2>
                        {{card.answer}}
                    </h2>

                    <button class="button-white button-clear button-large">
                        FLIP
                        <i class="fas fa-sync-alt"></i>
                    </button>
                </div>
            </transition>
        </div>
      </div>


    <!-- Tabbar for switching views-tabs -->
    <f7-toolbar tabbar labels bottom>
      <f7-link link="#" tab-link-active icon-md="material:note" text="Cards"></f7-link>
      <f7-link @click="toScan"  icon-md="material:camera_alt" text="Scan"></f7-link>
    </f7-toolbar>
  </f7-page>
</template>

<style scoped>
/* Part of the code-pen example
- will be modified when I get to this part of the project */

.red {
    background-color: #db4d52;
}

.gray {
    background-color: #6b6860;
}

/* Custom */

.button-white {
    background-color: white;
}

.button-white.button-clear {
    color: #000000;
    opacity: .2;
}

.button-large {
    font-size: 1.4rem;
    height: 4.5rem;
    line-height: 4.5rem;
    padding: 0 2rem;
}

ul.unstyled {
    list-style: none;
    padding: 0;
    margin: 0;
}

.card {
    transition: transform .5s;
    line-height: 1.5;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 90%;
    height: 100%;
    padding: 2rem;
    border-radius: 5px;
    margin: 0 1rem;
}

.card:hover {
    transform: scale(1.1);
}

.flex-grid-thirds {
    display: flex;
    justify-content: space-between;
}

.flex-grid-thirds .col {
    width: 32%;
}

.card-text h2 {
    color: #ffffff;
    opacity: .5;
    font-size: 1.5rem;
}

.flip-enter-active {
    transition: all .4s ease;
}

.flip-enter {
    transform: rotateY(180deg);
    opacity: 0;
}

.flip-leave {
    display: none;
}

@media (max-width: 600px) {
    .flex-grid-thirds {
        display: block;
    }
    .flex-grid-thirds .col {
        width: 100%;
        margin: 0 0 10px 0;
    }
}
</style>

<script>
import routes from '../js/routes.js';
import firebase from 'firebase';
import { db } from '../js/app';
import { client } from '../js/app'
import { firebaseApp } from '../js/app';
import axios from 'axios'
import dropdown from 'vue-dropdowns'
import 'firebase/auth';
const query = 'SELECT question, answer FROM cards WHERE email = ? AND setname = ?';

export default {
  data() {
      return {
        email: firebase.auth().currentUser.email,  
        FlashSets: [],
        Flashset: '',
        object: {
          name: 'Flashcard Sets',
        },
        loadedCards: []
      };
    },
    mounted() {
    /**db.collection('flashcards').where('email','==',this.email).get().then((querySnapshot) => {
      querySnapshot.forEach((doc) => {
        this.FlashSets.push(doc.data());
      });
    });**/
    axios.post('http://127.0.0.1:5000/getSets/', {
              setname: null,
              subject: null,
              email: this.email, 
              fileID: null
            }).then((response)=>{
              console.log(response.data);
              for (var i = 0; i < response.data["sets"].length; i++) {
                  this.FlashSets.push({'name': response.data["sets"][i]})
                }
       })
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
      toAbout(){
        this.$f7.views.main.router.navigate('/about/');
      },
      selectMethod(payload){
        this.object.name = payload.setname;
      },
      flipCard: function(card) {
            card.flipped = !card.flipped;
      },
      loadCards(event){
        axios.post('http://127.0.0.1:5000/getCards/', {
              setname: this.Flashset,
              subject: null,
              email: this.email, 
              fileID: null
            }).then((response)=>{
              console.log(response.data);
              for (var i = 0; i < response.data["cards"].length; i++) {
                  this.loadedCards.push(response.data["cards"][i]);
                }  
            })
      }
  }
}
</script>