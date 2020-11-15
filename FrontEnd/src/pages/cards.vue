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


    <!--Flash card template : -->
    <div id="flashCardApp" class="container flex-grid-thirds">
    <div v-for="card in cards" v-bind:key="card.id" v-bind:class="card.colorClass" class="card card-front">
            <transition name="flip">
                <div v-show="!card.flipped" @click="flipCard(card)" class="card-text card-front-text">
                    <h2>
                        {{card.frontText}}
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
                        {{card.backText}}
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




.green {
    background-color: #084C61;
}

.red {
    background-color: #db4d52;
}

.yellow {
    background-color: #f9cf3b;
}

.blue {
    background-color: #49b0e4;
}

.purple {
    background-color: #996ce2;
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
    font-size: 2.2rem;
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
        cards: [{
            id: 1,
            frontText: 'Who invented the first computer in the world?',
            backText: 'Konrad Zuse in 1936 by the name Z1',
            colorClass: 'red',
            flipped: false
        },
        {
            id: 2,
            frontText: 'Who invented all the parts that are now used for a modern computer?',
            backText: 'A man by the name of Charles Babbage in 1833.',
            colorClass: 'gray',
            flipped: false
        },
        {
            id: 3,
            frontText: 'Who invented the "Clarke Calculator"?',
            backText: 'Edith Clarke in 1925',
            colorClass: 'blue',
            flipped: false
        },
        {
            id: 4,
            frontText: 'Joe ?',
            backText: 'Joe mamma',
            colorClass: 'red',
            flipped: false
        }],
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
      flipCard: function(card) {
            card.flipped = !card.flipped;
      }
  }
}
</script>