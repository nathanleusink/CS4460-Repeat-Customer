###
# Title: order_info
###

import random

class order:

    def __init__(self, order_number, customer_ID):

        self.order_num = order_number
        self.customer = customer_ID
        self.order = []

    def get_order_value(self):
        return self.order
    
    def get_customer(self):
        return self.customer

    def get_order_num(self):
        return self.order_num

    def set_customer(self, new_ID):
        self.customer = new_ID

    def set_order_num(self, new_num):
        self.order_num = new_num

    def generate_random_order(self):
        #Generate a random order of meat, cheese, and veggies
        self.order = []
        i = ingredients()
        meat = i.choose_one_meat()
        cheese = i.choose_one_cheese()
        veggie = i.choose_one_veggie()
        self.order.append(meat)
        self.order.append(cheese)
        self.order.append(veggie)
        
        
class ingredients:

    def __init__(self):
        self.meat_options = ["Turkey", "Ham", "Roast Beef"]
        self.cheese_options = ["Swiss", "American", "Pepper Jack"]
        self.veggie_options = ["Lettuce", "Tomato", "Cucumber", "Spinach"]

    def choose_one_meat(self):
        meat = random.choice(tuple(self.meat_options))
        return meat
    
    def choose_one_cheese(self):
        cheese = random.choice(tuple(self.cheese_options))
        return cheese
    
    def choose_one_veggie(self):
        veggie = random.choice(tuple(self.veggie_options))
        return veggie

        
