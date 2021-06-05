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
