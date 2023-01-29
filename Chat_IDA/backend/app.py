from datetime import datetime
from sqlite3 import Connection
from transformers import BloomForCausalLM
from transformers import BloomTokenizerFast
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__, static_folder='./dist/assets',  template_folder='./dist')
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
app.secret_key = 'chatIDA'
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatIDA.db'
db = SQLAlchemy(app)

with app.app_context():

    class Users(UserMixin,db.Model):
        __tablename__ = "users"
        # Use Column to define a column. 
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(20), nullable=False)
        userConv = db.relationship('Conversation', backref='user')


        def __repr__(self) -> str:
            return f"<Users(id='{self.id}', email='{self.email}', password='{self.password}')>"

    @login_manager.user_loader
    def load_user(user_id):
        user = Users()
        user.id = user_id
        return user
   
    class Message(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        id_conv = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=True)
        msg_request = db.Column(db.Text(), nullable=False)
        msg_response = db.Column(db.Text(), nullable=False)
        timestamp = db.Column(db.DateTime)

   
    class Conversation(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.Text(), nullable= False)
        id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        message = db.relationship('Message', backref='conversation')



    db.create_all()

    tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-560m")
    model = BloomForCausalLM.from_pretrained("bigscience/bloom-560m")

#Récuperation des conversions 

    @app.route('/api/get_conversation', methods=['GET'])
    @login_required
    def get_conversations():
        conversations = Conversation.query.all()
        return jsonify([{'id': conversation.id, 'name': conversation.name, 'id_user': conversation.id_user } for conversation in conversations])
    


# Suppression d'une conversation
    @app.route('/api/delete_conversation/<int:id>', methods=['DELETE'])
    def delete_conversation(id):
        conversation = Conversation.query.get(id)
        db.session.delete(conversation)
        db.session.commit()
        return jsonify({'id': id})



#Récuperation des messages existants

    @app.route('/api/get_messages', methods=['GET'])
    @login_required
    def get_messages():
        id_conv= session['conv_id']
        messages= Message.query.filter_by(id_conv=id_conv).all()
        return jsonify([{'id': message.id, 'id_conv': message.id_conv, 'msg_request': message.msg_request, 'msg_response': message.msg_response , 'timestamp': message.timestamp} for message in messages])

#Récuperer une conversation à travers l'id de l'utilisateur
    @app.route('/api/get_conversation_by_id', methods=['POST'])
    @login_required
    def get_conversation_by_id():
        conversation_id = request.json['conv']
        session['conv_id'] = conversation_id
        return jsonify({'id_conv': conversation_id})


# Ajout d'une conversation
    @app.route('/api/add_conversation', methods=['POST'])
    @login_required
    def add_conversation():
        data = request.json['name']
        id_user = current_user.id
        conversation = Conversation(name=data, id_user=id_user)
        db.session.add(conversation)
        db.session.commit()
        return jsonify({'id': conversation.id, 'name': conversation.name, 'id_user': id_user})


#Inscription d'un nouvel utilisateur
    @app.route("/api/submitForm_register", methods=["POST"])
    def submitForm_register():
        email = request.json['email']
        password = request.json['password']
        user = Users.query.filter_by(email = email, password=password).first()

        if user:
            return jsonify({"message": "User already exists"}), 400
        if (email != '' and password != '') :
            users = Users(email=email, password=password)
            db.session.add(users)
            db.session.commit()
        print(email, password)
        return jsonify({"message": "User created successfully"}), 201


#connexion
    @app.route("/api/submitForm_login", methods=["POST"])
    def submitForm_login():
        email = request.json['email']
        password = request.json['password']
        user = Users.query.filter_by(email=email, password=password).first()
        if user:
            user = Users()
            user.id = email
            login_user(user)
            return jsonify({"message": "User found"}), 200
        else:
        # user not found
            print("User not found")
            return jsonify({"message": "User not found"}), 401

# Deconnexion
    @app.route('/api/logout')
    @login_required
    def logout():
        logout_user()
        return jsonify({"message": "Vous avez été déconnecter"}), 200
        
   
# Géneration de reponse et sauvegarde du message dans la base de données
    @app.route('/api/getResponse', methods=[ 'POST'])
    def getResponse():
        chatbot_prompt = """
Q: Bonjour
A: Bonjour, comment puisse-je t'aider ?
Q: Qui es-tu ?
A: Je suis un chatbot créé par IDA
Q: De quoi t'es capable ?
A: Je suis capable de répondre à des questions de manière pertinentes dans les plus brefs délais
<conversation history>
Q: <user input>
A: """
        # Get the user input request.get_json()['text']
        user_input = request.json['message']
        conversation_history=''
        result_length = 50
        chatbot_prompt= chatbot_prompt.replace("<conversation history>", conversation_history)
        chatbot_prompt= chatbot_prompt.replace("<user input>", user_input)


        inputs = tokenizer(chatbot_prompt, return_tensors="pt")
        inputSize = len(inputs["input_ids"][0])
        responseToken = model.generate(inputs["input_ids"],
                        max_new_tokens=result_length, 
                        num_beams=2, 
                       no_repeat_ngram_size=2,
                       early_stopping=True
                        )[0]
        response= tokenizer.decode(responseToken[inputSize:])
        response = response.split("Q:")[0]

        message_sent=user_input
        message_received=response
        timestamp = datetime.now()
        
        id_conv= session['conv_id']
      
        new_message = Message(id_conv = id_conv, msg_request = message_sent, msg_response = message_received, timestamp=timestamp)
        db.session.add(new_message)
        db.session.commit()

        return jsonify(response=response)

    
    if __name__ == '__main__':
        app.run(port= 4000, debug= True)