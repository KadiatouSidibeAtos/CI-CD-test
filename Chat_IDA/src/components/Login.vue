<template>
  <div id="app">
    <v-app :style="{ 'background-color': '#40414f' }">
      <v-app-bar app dark color="#343541">
        <!-- Header de notre page -->
        <v-toolbar-title class="header_title">ChatIDA</v-toolbar-title>
      </v-app-bar>
      <!-- Notre formulaire se trouve dans une balise V-content -->
      <v-content align-center fill-height class="login_form">
        <!-- Le formulaire est composé de deux parties: 
        une partie gauche permettant de log in ou se d'inscrire et
        une partie droite permettant d'aller sur la page de log in si l'utilisateur avait déjà un 
        compte et qu'il était sur la page d'inscription et vis versa -->
        <div class="formulaire_login_register_setup">
          <!-- Partie gauche -->
          <div>
            <v-card width="600" class="pa-4 text-center secondary rounded-0 text-black" :style="{ 'background-color': '#f8f9fa' }">
              <v-card-title>Bienvenue sur ChatIDA!</v-card-title>
              <p class="login_register_instructions" v-if="page == 'login'">
                To login, please enter the mail and password used during
                registration
              </p>
              <p class="login_register_instructions" v-else>
                To create an account, please enter your mail and password!
              </p>

              <v-card-text>
                <v-form v-model="valid" ref="form">
                  <v-text-field label="Email" v-model="email" required :rules="login_registerEmailRules"></v-text-field>
                  <v-text-field label="Password" v-model="password" type="password" required
                    :rules="[rules.required, rules.min]" hint="At least 8 characters"></v-text-field>
                  <v-btn v-if="page == 'login'" type="submit" @click.prevent="submitForm_login" :disabled="!valid"
                    :style="{ 'background-color': '#274c77', color: 'white' }" class="login_register_btn">
                    <v-icon left :style="{ color: 'white' }" class="login_register_icon">mdi-lock</v-icon>
                    Log in
                  </v-btn>
                  <v-btn v-else type="submit" @click.prevent="submitForm_register"  :disabled="!valid"
                    :style="{ 'background-color': '#052f5f', color: 'white' }" class="login_register_btn">
                    <v-icon class="login_register_icon">mdi-account</v-icon>Register</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </div>
          <!-- Partie droite -->
          <div class="formulaire_right">
            <v-card width="600" class="pa-4 text-center secondary rounded-0" :style="{ 'background-color': '#052f5f' }">
              <v-card-title v-if="page == 'login'" class="form_right_card_register_login_txt">Don't have an
                account?</v-card-title>
              <v-card-title v-else class="form_right_card_register_login_txt">Already have an account?</v-card-title>

              <p v-if="page == 'login'" class="form_right_desc_txt">
                Register and start chatting now!
              </p>
              <p v-else class="form_right_desc_txt">
                Log in and start your chat!
              </p>

              <v-img src="../../src/assets/ChatIDALogo.png" class="chatidalogo"></v-img>

              <v-btn v-if="page == 'login'" @click="return_to_register" class="form_right_register_login_btn" style="
                  background-color: transparent;
                  border: 1px solid white;
                  color: white;
                ">Click here to register</v-btn>
              <v-btn v-else @click="return_to_login" class="form_right_register_login_btn" style="
                  background-color: transparent;
                  border: 1px solid white;
                  color: white;
                ">Click here to login</v-btn>
            </v-card>
          </div>
        </div>
        <!-- Gestion des alertes: Affichage d'une notification si le l'utilsateur a bien pu créer un compte ou pas -->
        <v-alert v-if="registrationSuccess == true && page == 'create'" type="success">
          <p>You have been registered successfully!</p>
        </v-alert>
        <v-alert v-if="registrationFailed == true && page == 'create'" type="error">
          <p>Registration failed, please try again.</p>
        </v-alert>
        <!-- Gestion des alertes: Affichage d'une notification si le l'utilsateur n'a pas pu login a son compte -->
        <v-alert v-if="loginFailed" type="error" dismissible>
          <p>Login failed, please try again.</p>
        </v-alert>
        <!-- Footer -->
        <v-footer :style="{ 'background-color': '#343541' }" class="footer" height="auto">
          <v-col class="text-center" cols="12">
            {{ new Date().getFullYear() }} —
            <strong>KADANGHA BARIKI Cristiona | SIDIBE Kadiatou</strong>
          </v-col>
        </v-footer>
      </v-content>
    </v-app>
  </div>
</template>

<!-- -------------------------------------------------------------------------------------------------------- -->


<script>
// Utilisation d'Axios pour faire appel à nos api dans le backend (app.py)
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
      loginFailed: false,
      isLogged: false,
      valid: true,
      // Variables permettant d'appliquer des règles afin de s'assurer que le mail soit cohérent (xxx@xxx)
      // et qu ele mot de passe contienne au moins 8 caracteres
      login_registerEmailRules: [
        (v) => !!v || "Required",
        (v) => /.+@.+\..+/.test(v) || "E-mail must be valid",
      ],
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => (v && v.length >= 8) || "Min 8 characters",
      },
    };
  },
  emit:
    ['isLogged'],

  // Fonction de gestion des logins
  methods: {
    async submitForm_login() {
      this.page = 'login';
      try {
        const response = await axios.post('/api/submitForm_login', { email: this.email, password: this.password });

        if (response.data.message === "User found") {
          this.loginSucess = true;
          this.isLogged = true;
          this.$emit('isLogged', true)
        } else {
          this.loginFailed = true;
        }
      }

      catch (error) {
        console.log(error);
        this.loginFailed = true;
        this.isLogged = false;
      }

    },

    // Gestion de la creation des comptes
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
    // Fonction permettant de retourner sur la page d'enregistrement
    return_to_register() {
      this.page = "create";
    },
    // Fonction permettant de retourner sur la page de login

    return_to_login() {
      this.page = "login";
    },
  },
};
</script>


<!-- -------------------------------------------------------------------------------------------------------- -->
<style>
.login_form {
  background-color: #40414f;
}

.divider {
  margin-top: 20px;
  padding-top: 10px;
}

.header_title {
  color: white;
}

.login_register_instructions {
  padding-left: 15px;
  padding-bottom: 5px;
}

.login_register_icon {
  margin-right: 3px;
  padding-right: 10px;
}

.formulaire_login_register_setup {
  display: flex;
  margin-top: 80px;
  justify-content: center;
  flex-direction: row;
  flex-wrap: wrap;
}

.form_right_card_register_login_txt {
  color: white;
  height: fit-content;
}

.chatidalogo {
  /* width:350px; */
  height: 194px;
}

.form_right_desc_txt {
  color: white;
}

.form_right_register_login_btn {
  margin-bottom: 9px;
  background-color: transparent;
  color: white;
  border: 1px solid white;
}

.formulaire_right {
  margin-bottom: 5%;
}

.login_register_btn {
  margin-top: 10px;
}

.text-center {
  color: white;
}
</style>
