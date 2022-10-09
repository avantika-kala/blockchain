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
    response = {
        'message' : 'transaction added'
    }
    return jsonify(response)

@app.route('/user/add', methods=['POST'])
def add_user():
    values = request.get_json()
    userID = blockchain.add_user(values['Name'])
    response = {
        'message' : 'user successfully created',
        'userID' : userID + ' (Please note this for future transactions)'
    }
    return jsonify(response)

@app.route('/property/add', methods=['POST'])
def add_property():
    values = request.get_json()
    blockchain.add_property(values['OwnerID'], values['PropertyID'])
    response = {
        'message' : 'Owner and Property details added'
    }
    return jsonify(response)

@app.route('/peer/add', methods=['POST'])
def add_peer():
    values = request.get_json()
    peerList = blockchain.add_peer(values['Socket'], values['Stake'])
    response = {
        'message' : 'Peer added',
        'peerList' : peerList
    }
    return jsonify(response)



@app.route('/mine', methods=['POST'])
def mine():
    if len(blockchain.transactions) >= 2:
        chainLength = blockchain.new_block()  
        response = {
            'message' : 'New block added',
            'chainLength' : chainLength
        }
    else:
        response = {
            'message' : 'Less than 2 transactions present, cannot mine a block yet!'
        }
    return jsonify(response)