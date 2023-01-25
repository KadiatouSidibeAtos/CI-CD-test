<template>
  <v-app class="app">
    <div class="global" >
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
export default {
  components: {
    Homechat,
    Sidebar
  },
  data() {
    return {
    }
  },
  methods: {

  }
}
</script>
<style>

.global {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  background-color: #343541;
}

.sidebar {
  flex: 25%;
}

.homechat {
  flex: 75%;
}
</style>
