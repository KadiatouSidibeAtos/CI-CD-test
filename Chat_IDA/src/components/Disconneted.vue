<template>
  <div>

  </div>
  <div>
    <v-dialog v-model="showDialog">
      <v-card>
        <v-card-title>Deconnexion</v-card-title>
        <v-card-text>
          You are logged out, please refresh the page to reconnect.
          <v-btn color="green"   variant="solo" append-icon="mdi-reload" @click="refreshPage"> Refresh</v-btn>

          <p>Attention! You can not do anything in reconnect!</p>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="refreshPage">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  data: () => ({
    showDialog: true
  }),
  methods: {
    refreshPage() {
      this.showDialog = false
      location.reload()
    }
  }
}
</script>
