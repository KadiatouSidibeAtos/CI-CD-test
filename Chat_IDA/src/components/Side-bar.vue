<template>
     <Disconneted  v-if="!isLoggedOut"/>
    <v-card>
        <v-layout >
            <v-app-bar app dark color="#343541"  >
                <v-img 
                src="../../src/assets/ChatIDALogo.png"
                class="chatidalogo"
              ></v-img>
                <v-btn color="white" variant="text" icon="mdi-logout" @click="logout"></v-btn>
            </v-app-bar>
            <v-main>
            </v-main>
        </v-layout>
    </v-card>
</template>


<script lang="ts">

import axios from 'axios';
import Disconneted from './Disconneted.vue';

export default {
    components: {
    Disconneted
  },
    data() {
        return {
            
            isLoggedOut: true,
            drawer: false,
            group: null,
            isLogged: true
        }
    },
    

    props: ['isLogged'],

    methods: {


        async logout() {
            try {
                await axios.get(`/api/logout`)
                this.isLoggedOut = false;

            } catch (error) {
                console.error(error)
            }
        },

    }
}
</script>

<style>

</style>