<template>

  <v-content class="containt">
    <v-container>
      <v-row class="rows">
        <v-col cols="12" md="10" offset-md="2" class="cols">
          <v-card  class="card-title">
            <v-card-title >
              ChatIDA
            </v-card-title>

          </v-card>
          <div v-if="isSend" class="reponse">
            <div v-for="(item, index) in chatHistory" :key="index">
              <p class="p-message" v-if="item.isUser" >{{ item.message }}</p>

              <v-card class="card" v-if="!item.isUser && item.message.length != 0">
                <v-card-text class="text-card">
                  <p v-if="!item.isUser">{{ item.message }}</p>
                </v-card-text>
              </v-card>
            </div>
          </div>

        </v-col>
      </v-row>
    </v-container>
  </v-content>

  <v-footer class="footer" app bottom fixed padless  v-bind:style="{ backgroundColor: '#343541' }">
    <v-row align="center">
      <v-col cols="12">
        <v-text-field class="text-field"  :loading="isRequest" v-model="message" label="Enter your message" variant="solo" append-inner-icon="mdi-send"
          @keyup.enter="sendMessage"></v-text-field>
      </v-col>
    </v-row>
  </v-footer>

</template>

<script >
import axios from 'axios'
export default {
  data() {
    return {
      message: '',
      chatHistory: [],
      isSend: false,
      response: [],
      isRequest: false,
      backgroundColor: '#40414f'
    }
  },
  methods: {
    sendMessage() {
      this.isRequest = true;
      this.getResponse();
      this.isSend = true;
      if (this.message.trim() === '') return
      this.chatHistory.push({ message: this.message, isUser: true })
      this.message = ''


    },
    async getResponse() {
      if (this.message) {
        const { data } = await axios.post('http://localhost:4000/getResponse', { message: this.message });
        this.chatHistory.push({ message: data.response, isUser: false });
        this.isRequest = false;

      }

    }
  }
}
</script>
<style>
.containt {
  display: flex;
  justify-content: center;
}

.card-title{
  margin-right: 20%;
  margin-left: -25%;
  width: 20%;
  margin-bottom: 30px;
}

.reponse {
  margin-top: 20px;
  margin-right: 20%;
  margin-left: -10%;


}
.card{
  margin-top: 20px;
  background-color: #40414f;
  width:  100%;
}
.text-card{
  background-color: #40414f;
  color: white;
}
.p-message {
  margin-top: 20px;
  color: white;
}

.footer {
  display: flex;
  justify-content: center;
  margin-top: 25%;
  margin-bottom: 30px;

}

.text-field {
  color: white;
  border: 0px;
  border-radius: 7px;
  padding-bottom: -30px;
  margin-top: 10%;
  position: fixed;
  bottom: 0;
  width: 90%;
  margin-left: 30px;
  z-index: 1;
}
</style>
