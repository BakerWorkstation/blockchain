'''
@Author: your name
@Date: 2020-06-18 15:08:08
@LastEditTime: 2020-06-18 15:17:19
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /root/10.py
'''
from uuid import uuid4
from flask import Flask
from blockchain import Blockchain

app = Flask(__name__)
blockchain1 = Blockchain()
 
node_identifier = str(uuid4()).replace("-","")
 
@app.route("/index", methods=['GET'])
def index():
    return "Hellp BlockChain"
 
 
@app.route('/transanctions/new', methods=['POST'])
def new_transaction():
    value = request.get_json()
    requested = ["sender", "recipient", "amount"]
 
    if value is None:
        return "Missing values", 400
 
    if not all(k in value for k in requested):
        return "Missing values", 400
 
    index = blockchain1.new_transaction(value["sender"],
                                       value["recipient"],
                                       value["amount"])
 
    reponse = {"message": f'Transaction wille be add in {index}'}
 
    return jsonify(reponse), 201
 
 
@app.route('/mine', methods=['GET'])
def mine():
 
    last_block = blockchain1.last_block
    last_proof = last_block["proof"]
 
    proof = blockchain1.proof_work(last_proof)
    blockchain1.new_transaction(sender="0",recipient=node_identifier,                      amount=1 )
    block = blockchain1.new_block(proof,None)
 
    reponse = {
        'index': block["index"],
        'timestamp': block['timestamp'],
        'transcations': block['transcations'],
        'proof':  block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(reponse), 200
 
 
@app.route('/chain', methods=['GET'])
def full_chain():
    reponse = {
        'chain': blockchain1.chain,
        'length': len(blockchain1.chain)
    }
    return jsonify(reponse), 200
 
 
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
