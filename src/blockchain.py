from datetime import datetime
import uuid

class Blockchain:

    def __init__(self):
        self.transactions = []
        self.chain = []
        self.users = dict() # key=UserID and value=name
        self.property = dict() # key=PropertyID and value=owner
    
    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, sellerID, buyerID, propertyID):
        self.transactions.append({

            'SellerID' : sellerID,
            'BuyerID' : buyerID,
            'PropertyID' : propertyID,
            'timestamp' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        #TODO - code to check if the seller buyer and property are registered with the system

        for t in self.transactions:
            print(t)

        return True
    
    def add_user(self, name):
        id = uuid.uuid4().hex
        self.users[id] = name
        return id

    def add_property(self, ownerID, propertyID):
        self.users[propertyID] = ownerID
        return True
