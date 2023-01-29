<template>
  <v-container fluid>
    <v-row>
      <v-col cols="3" md="3" class="side">
        <div class="scrollable-div">
          <v-btn prepend-icon="mdi-plus" color="white" variant="outlined" style="margin-bottom: 5px;"
            @click="dialog = true">
            Add Conversation
          </v-btn>
          <v-divider color="white"></v-divider>
          <div v-for="conversation in conversations" :key="conversation.id">
            <v-btn color="white" class="text-left" @click="getConversationById(conversation)" prepend-icon="mdi-message"
              variant="text">
              {{ conversation.name }}
              <template v-if="showDeleteIcon">
                <v-icon @click="deleteConversation(conversation)" color="red" class="ml-2">mdi-delete</v-icon>
              </template>
            </v-btn>
          </div>
        </div>

      </v-col>
      <v-col cols="9" md="9" class="chatbot">
        <v-text-field class="text-field" :loading="isRequest" v-model="message" label="Enter your message"
          variant="solo" append-inner-icon="mdi-send" @keyup.enter="sendMessage"></v-text-field>

        <div>

          <div v-for="message in messages" :key="message.id">
            <v-row>

              <v-col cols="11" style="text-align: right; ">
                <v-card max-width="70%" class="mx-auto float-right">
                  <v-card-text>
                    {{ message.msg_request }}
                  </v-card-text>
                  <v-card-subtitle>
                    {{ message.timestamp }}
                  </v-card-subtitle>
                </v-card>
                <!-- <p class="p-message">{{ message.msg_request }}</p> -->
              </v-col>
              <v-col cols="1" style="margin-top: 10px;">
                <v-avatar color="#C2CBCD">
                  <v-icon icon="mdi-account-circle"></v-icon>
                </v-avatar>
              </v-col>
            </v-row>

            <div v-if="message.msg_response.length != 0">
              <v-row>
                <v-col cols="1" style="margin-top: 15px;">
                  <v-avatar color="#C2CBCD">
                    <v-img src="../../src/assets/ChatIDALogo.png" class="chatidalogo"></v-img>
                  </v-avatar>
                </v-col>
                <v-col cols="11">
                  <v-card max-width="70%" class="mx-auto float-left">
                    <v-card-text class="text-card">
                      {{ message.msg_response }}
                    </v-card-text>
                    <v-card-subtitle>
                      {{ message.timestamp }}
                    </v-card-subtitle>
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
      isRequest: false,
      messages: [],
      showDeleteIcon: false,
      dialog: false,
      conversations: [],
    }
  },
  mounted() {
    this.getConversations()
    this.getMessages();
  },
  methods: {
    sendMessage() {
      this.question = this.message;
      this.isSend = true;
      this.isRequest = true;
      this.getResponse();
      this.message = ''

    },

    async getResponse() {
      if (this.message) {
        try {
          const { data } = await axios.post('/api/getResponse', { message: this.message });
          this.getMessages();
          this.isSend = false;
          this.question = ''
          this.isRequest = false;
        } catch (error) {
          console.error(error)
        }
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
.side {
  background-color: #40414f;
  margin-top: -4px;
  margin-left: -4px;
}
</style>
