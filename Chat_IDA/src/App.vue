<template>
  <v-app >
    <v-main v-if="!isLogged" >
      <Login  @isLogged="changeLogStatus"/>
    </v-main>
    <div class="global"  v-if="isLogged">
      <div class="sidebar">
        <Sidebar @messages_test="getMessage" v-bind:isLogged="isLogged" />
      </div>
      <div class="homechat">
        <Homechat />
      </div>
    </div>
  </v-app>

</template>

<script>
import Homechat from './components/Home-chat.vue'
import Sidebar from './components/Side-bar.vue'
import Login from './components/Login.vue'
export default {
  components: {
    Homechat,
    Sidebar,
    Login
  },
  data() {
    return {
      isLogged:false,
      messages_test: []
    }
  },
 
  methods: {
    changeLogStatus(isLogged){
      this.isLogged=isLogged;
    },
   
  }
}
</script>
<style>

</style>
