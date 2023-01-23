<template>

  <v-content class="side">
    <v-container>
      <v-row>
        <v-col cols="12" md="8" offset-md="2">
          <v-card>
            <v-card-title>
              ChatIDA
            </v-card-title>
            <v-card-text>
              <v-form ref="form">
                <v-text-field v-model="message" label="Saisir votre message ici"></v-text-field>
                <v-btn @click="sendMessage">Envoyer</v-btn>
              </v-form>

            </v-card-text>
          </v-card>
          <div v-if="isSend" class="reponse">
            <div v-for="(item, index) in chatHistory" :key="index">
              <p v-if="item.isUser">{{ item.message }}</p>
            </div>
            <v-card class="card">
              <v-card-text>
                <div v-for="(item, index) in chatHistory" :key="index">
                  <p v-if="!item.isUser">{{ item.message }}</p>
                </div>
              </v-card-text>
            </v-card>
          </div>

        </v-col>
      </v-row>
    </v-container>
  </v-content>
</template>

<script lang="ts">
export default {
  data() {
    return {
      message: '',
      chatHistory: [],
      isSend: false
    }
  },
  methods: {
    sendMessage() {
      this.isSend = true;
      if (this.message.trim() === '') return
      this.chatHistory.push({ message: this.message, isUser: true })
      this.message = ''
      this.getResponse()
      
    },
    getResponse() {
      // Make an API call to your chatbot here to get the response
      // and push it to the chatHistory array
      this.chatHistory.push({ message: 'Hello, how can I help you today?', isUser: false })
    }
  }
}
</script>
<style>
.side {
  background-color: red;
}

.reponse, .card{
  margin-top:  20px;
}
</style>
