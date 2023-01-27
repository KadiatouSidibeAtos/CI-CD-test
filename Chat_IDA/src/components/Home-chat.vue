<template>

    <v-container>
      <v-row class="rows" align="center">
        <v-col cols="12" md="10" offset-md="2" class="cols">
          <div v-if="isSend" class="reponse">
            <div v-for="(item, index) in chatHistory" :key="index">
              <v-row>
                <v-col cols="1" style="margin-top: 10px;">
                  <v-avatar color="#C2CBCD" v-if="item.isUser">
                    <v-icon v-if="item.isUser" icon="mdi-account-circle"></v-icon>
                  </v-avatar>
                </v-col>
                <v-col cols="11">
                  <p class="p-message" v-if="item.isUser">{{ item.message }}</p>
                </v-col>
              </v-row>


              <div v-if="!item.isUser && item.message.length != 0">
                <v-row>
                  <v-col cols="1" style="margin-top: 15px;">
                    <v-avatar color="#C2CBCD" v-if="!item.isUser">
                      <span class="text-h5">CB</span>
                    </v-avatar>
                  </v-col>
                  <v-col cols="11">
                    <v-card class="card">
                      <v-card-text class="text-card">
                        <p v-if="!item.isUser">{{ item.message }}</p>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>


              </div>


            </div>
          </div>

        </v-col>
      </v-row>
    </v-container>


  <v-footer class="footer" app bottom fixed padless v-bind:style="{ backgroundColor: '#343541' }">
    <v-row align="center">
      <v-col cols="12">
        <v-text-field class="text-field" :loading="isRequest" v-model="message" label="Enter your message"
          variant="solo" append-inner-icon="mdi-send" @keyup.enter="sendMessage"></v-text-field>
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
        const { data } = await axios.post('/api/getResponse', { message: this.message });
        if(data.response){
          this.chatHistory.push({ message: data.response, isUser: false });
        }else{
          this.chatHistory.push({ message: "Désolé, je n'ai pas bien compris votre question", isUser: false });
        }
        
        this.isRequest = false;

      }      

    },

    // async saveConversation() {
    //   if (this.chatHistory && this.chatHistory.length!=0) {
    //     axios.post('/api/saveConversation', { chatHistory: this.chatHistory })
    //     .then(response => {
          
    //     })
    //     .catch(error => {
    //       console.log(error);
    //     });

    //   }      

    // },
    
  }
}
</script>
<style>
.containt {
  display: flex;
  justify-content: center;
}

.card-title {
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

.card {
  margin-top: 20px;
  width: 100%;
}

.text-card {
  background-color: #343541;
  color: white;
  border: 0px;
 
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
