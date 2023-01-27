<template>
    <div class="side">
        <v-card height="100%" width="30%">
            <v-navigation-drawer permanent class="bg-color" style="background-color: #343541; color: white;">
                <v-list-item>
                    <v-list-item-content>
                        <v-list-item-title class="text-h6">
                            ChatIDA
                        </v-list-item-title>
                        <v-list-item-subtitle>
                            Projet chatbot M2
                        </v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>

                <v-divider></v-divider>
                <div>
                    <v-btn prepend-icon="mdi-plus" variant="outlined" class="conv" @click="dialog = true">
                        Add Conversation
                    </v-btn>
                    <v-btn block class="conv" variant="text" prepend-icon="mdi-message">
                        Conversation 1
                    </v-btn>
                    <v-btn block class="conv" variant="text" prepend-icon="mdi-message">
                        Conversation 2
                    </v-btn>
                    <v-btn block class="conv" variant="text" prepend-icon="mdi-message">
                        Conversation 3
                    </v-btn>
                </div>
                <template v-slot:append>
                    <div class="pa-2" style="text-align: left;">
                        <v-btn block variant="text" style="text-align: left;" prepend-icon="mdi-logout">
                            Logout
                        </v-btn>
                    </div>
                </template>
            </v-navigation-drawer>
        </v-card>
    </div>

    <div class="text-center">
        <v-dialog v-model="dialog">
            <v-card>
                <v-card-text>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                    et dolore magna aliqua.
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" block @click="dialog = false">Close Dialog</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>

</template>

<script lang="ts">
export default {
    data() {
        return {
            items: [
                { title: 'Dashboard', icon: 'mdi-view-dashboard' },
                { title: 'Photos', icon: 'mdi-image' },
                { title: 'About', icon: 'mdi-help-box' },
            ],
            right: null,
            dialog: false,
        }
    },
}
</script>

<style>
.side {
    background-color: #343541
}

.conv {
    margin: 5px;
    text-align: left;
}

.conv:hover {
    border: 2px;
    border-radius: 5px;
    background-color: 40414f;
}
</style>