from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/', methods=['GET'])
def test():
    return '<h1>Land Management System</h1>'

@app.route('/transaction/add', methods=['POST'])
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
def add_property():
    values = request.get_json()
    blockchain.add_property(values['OwnerID'], values['PropertyID'])
    return 'Owner and Property details added'

@app.route('/mine', methods=['POST'])
def mine():
    if len(blockchain.transactions) >= 2:
        blockchain.new_block()  
        return 'Block added'
    else:
        return 'Less than 2 transactions present, cannot mine a block yet!'