from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/', methods=['GET'])
def test():
    return '<h1>Land Management System</h1>'

@app.route('/transaction', methods=['POST'])
def add_transaction():
    values = request.get_json()
    blockchain.add_transaction(values['BuyerID'], values['SellerID'], values['PropertyID'])
    return  'transaction added'

@app.route('/user/add', methods=['POST'])
def add_user():
    values = request.get_json()
    userID = blockchain.add_user(values['Name'])
    return 'user created with id - ' + userID + '\n Please note this for future transactions'

@app.route('/property/add', methods=['POST'])
def add_user():
    values = request.get_json()
    blockchain.add_user(values['OwnerID'], values['propertyID'])
    return 'Owner and Property details added'


