<template>
    <v-card>
        <v-layout>
            <!-- <v-system-bar color="deep-purple darken-3"></v-system-bar> -->

            <v-app-bar color="primary" prominent>
                <v-img 
                src="../../src/assets/ChatIDALogo.png"
                class="chatidalogo"
              ></v-img>
                <v-btn variant="text" icon="mdi-logout" @click="logout"></v-btn>
            </v-app-bar>

           

            <v-main >
            </v-main>
        </v-layout>
    </v-card>
</template>


<script lang="ts">

import axios from 'axios';

export default {
    data() {
        return {
            items: [
                {
                    title: 'Foo',
                    value: 'foo',
                },
                {
                    title: 'Bar',
                    value: 'bar',
                },
                {
                    title: 'Fizz',
                    value: 'fizz',
                },
                {
                    title: 'Buzz',
                    value: 'buzz',
                },
            ],
            isLoggedOut: false,
            drawer: false,
            group: null,
        }
    },
    watch: {
      group () {
        this.drawer = false
      },
    },

    props: ['isLogged'],

    methods: {


        async logout() {
            try {
                await axios.get(`/api/logout`)
                this.getConversations()
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
.side {
    background-color: #343541
}

.conv {
    margin: 5px;
    text-align: left;
}

.conv:hover {
    border: 2px;
    border-radius: 5px;
    background-color: 40414f;
}

.text-left {
    text-align: left;
}
</style>