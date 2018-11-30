# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 23:11:42 2018

@author: Rishi Varun
"""

import datetime
from flask import Flask, jsonify 
import json
import hashlib

#build the blockchain 
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        
        block = {'index': len(self.chain) - 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        
        self.chain.append(block)
        return block 
    
    def proof_of_work(self, previous_proof):
        new_proof = 1 
        check_proof = False 
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def hash_alg(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1 
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash_alg(previous_block):
                return False 
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
        return True 
    
# call for webapp 
        
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods = ['GET'])
def mine():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash_alg(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'block mined for sure',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200 

@app.route('/isvalid', methods = ['GET'])
def isvalid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'the given blockchain is valid bro dont worry'}
    else:
        response = {'message': 'the blockchain has been slayed lol no trust bro'}
    return jsonify(response)


app.run(host = '', port = 5000)


    
    
    
        
    
