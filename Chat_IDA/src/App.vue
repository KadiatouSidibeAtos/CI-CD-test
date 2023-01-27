<template>
  <v-app class="app">
    <v-main v-if="!isLogged" style="background-color: black;">
      <Login  @isLogged="changeLogStatus"/>
    </v-main>
    <div class="global" v-if="isLogged">
      <div class="sidebar">
        <Sidebar />
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
      isLogged:false
    }
  },
  methods: {
    changeLogStatus(isLogged){
      this.isLogged=isLogged;
    }
  }
}
</script>
<style>

.global {
  flex: 1;
  display: flex;
  background-color: #40414f;
}

.sidebar {
  flex: 25%;
}

.homechat {
  flex: 75%;
}
</style>
