<template>
    <v-card>
        <v-layout >
            <v-app-bar color="#1F505B"  prominent class="app-bar" >
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

export default {
    data() {
        return {
            
            isLoggedOut: false,
            drawer: false,
            group: null,
        }
    },
    

    props: ['isLogged'],

    methods: {


        async logout() {
            try {
                await axios.get(`/api/logout`)
                this.isLoggedOut = true;
                this.isLogged = false;
            } catch (error) {
                console.error(error)
            }
        },

        async getMessages() {
            try {
                const { data } = await axios.get('/api/get_messages')
                this.messages = data
            } catch (error) {
                console.error(error)
            }
        },
    }
}
</script>

<style>

</style>