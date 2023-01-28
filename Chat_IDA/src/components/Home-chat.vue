<template>
  <v-container>
    <v-row>
      <v-col cols="3" md="3">
        <div class="scrollable-div">
          <v-btn prepend-icon="mdi-plus" variant="outlined" class="conv" @click="dialog = true">
            Add Conversation
          </v-btn>
          <div v-for="conversation in conversations" :key="conversation.id">
            <v-btn class="text-left" @click="getConversationById(conversation)" prepend-icon="mdi-message"
              variant="text">
              {{ conversation.name }}
              <template v-if="showDeleteIcon">
                <v-icon @click="deleteConversation(conversation)" color="red" class="ml-2">mdi-delete</v-icon>
              </template>
            </v-btn>
          </div>
        </div>

      </v-col>
      <v-col cols="9" md="9">
        <v-text-field class="text-field" :loading="isRequest" v-model="message" label="Enter your message"
          variant="solo" append-inner-icon="mdi-send" @keyup.enter="sendMessage"></v-text-field>

        <div class="scrollable-div">
          <div v-for="message in messages" :key="message.id">
            <v-row>
              <v-col cols="1" style="margin-top: 10px;">
                <v-avatar color="#C2CBCD">
                  <v-icon icon="mdi-account-circle"></v-icon>
                </v-avatar>
              </v-col>
              <v-col cols="11">
                <p class="p-message">{{ message.msg_request }}</p>
              </v-col>
            </v-row>

            <div v-if="message.msg_response.length != 0">
              <v-row>
                <v-col cols="1" style="margin-top: 15px;">
                  <v-avatar color="#C2CBCD">
                    <span class="text-h5">CB</span>
                  </v-avatar>
                </v-col>
                <v-col cols="11">
                  <v-card class="card">
                    <v-card-text class="text-card">
                      <p>{{ message.msg_response }}</p>
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



  <div class="text-center">
    <v-dialog v-model="dialog">
      <v-card>
        <v-card-text>
          <v-form>
            <v-text-field v-model="contitle" label="Titre de la conversation" aria-required="true">
            </v-text-field>
            <v-btn @click="addConversation">Ajouter</v-btn>
          </v-form>

        </v-card-text>
      </v-card>
    </v-dialog>
  </div>


</template>


<script >
import axios from 'axios'
import SideBar from './Side-bar.vue'
export default {
  components: {
    SideBar
  },
  data() {
    return {
      message: '',
      chatHistory: [],
      isSend: false,
      response: [],
      isRequest: false,
      backgroundColor: '#40414f',
      messages: [],
      id_conv: 0,
      showDeleteIcon: false,
      dialog: false,
      conversations: [],
    }
  },
  props:
    ['messages_test'],
  created() {

    this.getConversations()
    console.log("concall " + this.conversations);
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
        this.getMessages();
        if (data.response) {
          this.chatHistory.push({ message: data.response, isUser: false });
        } else {
          this.chatHistory.push({ message: "Désolé, je n'ai pas bien compris votre question", isUser: false });
        }

        this.isRequest = false;

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

    async addConversation() {
      try {
        const { data } = await axios.post('/api/add_conversation', { name: this.contitle })
        this.contitle = ''
        this.getConversations()
        this.dialog = false;
      } catch (error) {
        console.error(error)
      }
    },

    async getConversations() {
      try {
        const { data } = await axios.get('/api/get_conversation')
        this.conversations = data
      } catch (error) {
        console.error(error)
      }
    },
    async deleteConversation(conversation) {
      try {
        await axios.delete(`/api/delete_conversation/${conversation.id}`)
        this.getConversations()
      } catch (error) {
        console.error(error)
      }
    },
    async getConversationById(conversation) {
      try {
        const { data } = await axios.post('/api/get_conversation_by_id', { conv: conversation.id })
        this.showDeleteIcon = !this.showDeleteIcon
        this.getMessages();
      } catch (error) {
        console.error(error)
      }
    },

  }
}
</script>
<style>
.scrollable-div {
  max-height: 400px;
  overflow-y: auto;
}


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
</style>
