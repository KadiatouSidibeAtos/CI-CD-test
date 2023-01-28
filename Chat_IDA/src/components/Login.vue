<template>
  <v-app>
    <v-app-bar height="50" app dark color="black">
      <v-toolbar-title v-if="page == 'login'">ChatIDA Login</v-toolbar-title>
      <v-toolbar-title v-else>ChatIDA Register</v-toolbar-title>
    </v-app-bar>
    <v-content align-center fill-height class="login_form">
      <v-card width="600" class="mx-auto mt-9">
        <v-card-title>Bienvenue sur chatIDA!</v-card-title>
        <v-card-text>
          <v-form v-model="login" ref="form">
            <v-text-field label="Email" v-model="email" required></v-text-field>
            <v-text-field label="Password" v-model="password" type="password" required></v-text-field>
            <v-btn v-if="page == 'login'" @click.prevent="submitForm_login()">Login</v-btn>
            <v-btn v-else @click.prevent="submitForm_register">Register</v-btn>

            <v-divider class="divider"></v-divider>

            <v-btn v-if="page == 'login'" @click="return_to_register">Don't have an account? Click here to
              register</v-btn>
            <v-btn v-else @click="return_to_login"> Already registered? Click here to login</v-btn>
          </v-form>
        </v-card-text>
      </v-card>

      <v-alert v-if="registrationSuccess == true && page == 'create'" type="success">
        <p>You have been registered successfully!</p>
      </v-alert>
      <v-alert v-if="registrationFailed == true && page == 'create'" type="error">
        <p>Registration failed, please try again.</p>
      </v-alert>


      <v-alert v-if="loginSuccess && page == 'login'" type="success">
        <p>You have been logged in successfully!</p>
      </v-alert>
      <v-alert v-if="loginFailed && page == 'login'" type="error">
        <p>Login failed, please try again.</p>
      </v-alert>

    </v-content>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  name: "Login",
  data() {
    return {
      page: "create",
      email: "",
      password: "",
      registrationSuccess: false,
      registrationFailed: false,
      loginSuccess: false,
      loginFailed: false,
      isLogged: false
    };
  },
  methods: {
    async submitForm_login() {
      this.page = 'login';
      try {
        const response = await axios.post('/api/submitForm_login', { email: this.email, password: this.password });
       
        if(response.data.message==="User found"){
          this.loginSucess=true;
          this.isLogged = true;
          this.$emit('isLogged', true)
        }else{
          this.loginFailed=true;
        }
      }

      catch (error) {
        console.log(error);
        this.loginFailed = true;
        this.isLogged=false;
      }

    },

    async submitForm_register() {
      this.page = 'create';
      try {
        const response = await axios.post('/api/submitForm_register',
          { email: this.email, password: this.password });
        console.log(response);
        if (response.data.message === "User created successfully") {
          this.registrationSuccess = true;
        } else {
          this.registrationFailed = true;
        }
      }
      catch (error) {
        console.log(error);
        this.registrationFailed = true;
      }

    },

    return_to_register() {
      this.page = 'create';
    },

    return_to_login() {
      this.page = 'login';
    }
  },
  emit:
    ['isLogged']
}

</script>
<style>
.login_form {
  margin-top: 50px;
}

.divider {
  margin-top: 20px;
  padding-top: 10px;
}
</style>
