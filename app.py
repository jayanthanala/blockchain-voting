import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.chain = []
        self.voterid =('sdkjs','uifhd','yfghu','ncdhd','iwjod','ehbfh','fkuhb','efhbh','ooajk','shate','qijsh') ## Voter IDs
        self.vidDone = []
        self.candidate = ("Kanye","Travis","Nicki Minaj","Lil Nas X")
        self.countVote = {}
        self.VotingTrans = []
        self.nodes = set()
        for i in range(len(self.candidate)):
            self.countVote.update({self.candidate[i]: 0})
        self.create_block(proof=1, previous_hash='0') ## Genesis Block
        
        def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'VotingTrans': self.VotingTrans
        }
        self.VotingTrans = []
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    
    def get_a_block(self, i):
        if i <= len(self.chain):
            return self.chain[i]
        return -1;

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, voter, candidate):
        if voter in self.voterid and candidate in self.candidate:
            if voter not in self.vidDone:
                self.VotingTrans.append(
                    {'voter': voter,
                     'candidate': candidate,
                     })
                self.vidDone.append(voter)
                # self.countVote[candidate]+=1
                previous_block = self.get_previous_block()
                return previous_block['index'] + 1
            else:
                return -1 ## Already Voted
        else:
            return None ## Candidate or Voter doesn't exist

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
    def getResult(self, chain):
        self.countVote = {};
        for i in range(len(self.candidate)):
            self.countVote.update({self.candidate[i]: 0})
        for b in chain:
            for j in b['VotingTrans']:
                self.countVote[j['candidate']] += 1
        return self.countVote
    
app = Flask(__name__)
node_address = str(uuid4()).replace('-', '')
blockchain = Blockchain()

# Getting the full Blockchain
@app.route('/get_chain')
def get_chain():
    response = {'chain': blockchain.chain,'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid')
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'No!! The Blockchain is not valid.'}
    return jsonify(response), 200

# Changing a block data to verify Blockchain's validity
@app.route('/change_data')
def mod_data():
    block = blockchain.get_a_block(1)
    if block == -1: 
        response = {'message': 'No Such Block exits in blockchain'}
    else:
        block["VotingTrans"][1]["candidate"] = "B"
        response = {'block': block,"msg":"Block Data Modified"}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/caste_vote', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['voter', 'candidate']
    if not all(key in json for key in transaction_keys):
        return 'Some required data for the transaction are missing', 400
    index = blockchain.add_transaction(json['voter'], json['candidate'])
    if index==None:
        return 'This is Voter ID/Candidate is Invalid'
    elif index==-1:
        return 'This is a Fake Vote, You\'ve already casted the vote'
    else:
        msg="Added to Pending Votes, yet to be mined"
        if len(blockchain.VotingTrans)==4:
            mine_block()
            msg = "A New Block is mined"
        response = {"msg":'This is a successful vote, Vote Casted',"Block Status":msg,"pendingVotes":blockchain.VotingTrans}
        return response,200
