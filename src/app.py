from flask import Flask, jsonify, request
from blockchain import Blockchain
import json

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/', methods=['GET'])
def test():
    return '<h1>Land Management System</h1>'

# ----------------------------- USER -----------------------------------
# Feature 1 - To register new users to the system with previously owned property
@app.route('/user/add', methods=['POST'])
def add_user():
    values = request.get_json()
    userID = blockchain.add_user(values['Name'])
    for p in  values['PropertyID']:
        blockchain.add_property(userID, p)
    response = {
        'message' : 'user successfully created',
        'userID' : userID + ' (Please note this for future transactions)'
    }
    return jsonify(response)
# ----------------------------- PROPERTY -----------------------------------
@app.route('/property/add', methods=['POST'])
def add_property():
    values = request.get_json()
    message = blockchain.add_property(values['OwnerID'], values['PropertyID'])
    response = {
        'message' : message
    }
    return jsonify(response)
# ----------------------------- NODES -----------------------------------
@app.route('/node/add', methods=['POST'])
def add_node():
    values = request.get_json()
    nodeList = blockchain.add_node(values['Socket'], values['Stake'])
    response = {
        'message' : 'node added',
        'nodeList' : nodeList
    }
    return jsonify(response)

# ----------------------------- MINING -----------------------------------
@app.route('/mine', methods=['POST'])
def mine():
    ip = request.server[0]
    port = request.server[1]
    if port in blockchain.witnesses:
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
    else:
        response = {
            'message' : 'User not authorized to block a mine!'
        }
    return jsonify(response)

# ----------------------------- DELEGATES -----------------------------------
@app.route('/delegate/add', methods=['POST'])
def add_delegate():
    values = request.get_json()
    message = blockchain.add_delegate(values['Socket'], values['Stake'])
    response = {
        'message' : message
    }
    return jsonify(response)

# ----------------------------- TRANSACTION -----------------------------------
# Feature 2 - The user should be able to buy and sell the property.
@app.route('/transaction/add', methods=['POST'])
def add_transaction():
    values = request.get_json()
    message =  blockchain.add_transaction(values['BuyerID'], values['SellerID'], values['PropertyID'])
    response = {
        'message' : message
    }
    return jsonify(response)

# Feature 5 - To be able to view the transaction history that is related to a property.
@app.route('/transaction/history', methods=['GET'])
def get_transaction_history():
    values = request.get_json()
    history = blockchain.get_transaction_history(values['PropertyID']) 
    if history:
        response = {
            'message' : 'Transaction history found!',
            'transactionHistory' : history
        }
    else:
        resposne = {
            'message' : 'Transaction history not found'
        }
    return jsonify(response)


# ----------------------------- BLOCKCHAIN & CONSENSUS-----------------------------------
# Feature 3 - To improve the security of the blockchain, incorporate a consensus algorithm DPoS
@app.route('/chain', methods=['GET'])
def get_local_chain():
    local_chain = blockchain.get_local_blockchain()
    response = {
        'chain': local_chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

@app.route('/voting', methods=['GET'])
def vote():
    witnesses = blockchain.initiate_voting()
    response = {
        'message' : 'voting completed',
        'witnesses' : witnesses
    }
    return jsonify(response)

@app.route('/chain/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_chain()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.get_local_blockchain()
        }
    return jsonify(response), 200
