###
# Title: customer_info
###

class customer:

    def __init__(self, customer_number):
        self.cust_ID = customer_number
        self.pso_score = 50

    def get_cust_ID(self):
        return self.cust_ID

    def get_pso_score(self):
        return self.pso_score

    def set_cust_ID(self, new_ID):
        self.cust_ID = new_ID

    def set_pso_score(self, new_score):
        self.pso_score = new_score
