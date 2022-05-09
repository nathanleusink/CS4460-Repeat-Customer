###
# Title: Master Control Script
###

#Importing Modules
import os
import sys
import time
import csv

#Importing Supporting Python Files
import customer_reaction as cust_react
import SandPSO as pso
import customer_info
import order_info
import vrep_controller as v
import ingredient_recognition as ir

#Getting Current Location
base_dir = os.getcwd()

#Globals
customer_number = 1
order_number = 1
customer_list = []
client_ID = 0

#Instances
order = order_info.order(order_number, customer_number)


def print_welcome():
    print("--------------------------------------------------------------")
    print("---      WELCOME TO REPEAT CUSTOMER VENDING MACHINE        ---")
    print("---                                                        ---")
    print("---   Authors: Jenna Chadwick, Kristen Farmer,             ---")
    print("---            Austin Spory, Nathan Leusink                ---")
    print("---                                                        ---")
    print("---                                                        ---")
    print("--------------------------------------------------------------")
    print("Version 1.0.0")
    print("Last Updated on 5/3/2022")
    print("\n\nTHE PROGRAM IS NOW STARTING...\n\n")

def initilization():

    global order_number, customer_number, order, client_ID

    #Initialize VREP
    print("[LOG] Verifying Connection with VREP")
    client_ID = v.system_initialize()

    #Training PSO
    print("[LOG] Training PSO...")
    test = pso.train("train.txt").best[0:-1] + pso.train("train.txt").best
    print("[LOG] PSO Trained")
    
    #Get Order
    order_number = order_number + 1
    order.generate_random_order()
    print("[LOG] Random Sandwich Order: ", order.get_order_value())
    

    

def add_new_customer():
    global customer_number, customer_list   

    print("[LOG] Adding New Customer with ID: ", customer_number)
    
    #instance of customer with id customer number
    cust = customer_info.customer(customer_number)

    #iterate customer number
    customer_number = customer_number + 1

    #add customer to customer list
    customer_list.append(cust)

    #Add new particle in PSO
    pso.make(customer_number)


def update_customer_satisfaction():
    global customer_number
    
    #Calculate Customer Satisfaction
    pso_change = cust_react.external_control_loop()

    #Changing algorithm
    pso.score(customer_number, pso_change)

    return pso_change

    
def control_loop():

    global customer_number, customer_list, data_logger

    

    #Train PSO First
    initilization()
    
    #Running Continuously
    while True:

        #Look for New Customer
        face_found = cust_react.recognizeFace()
        
        #If face found, create new particle
        if(face_found):
            
            #Make New Customer and Customer Particle 
            add_new_customer()

            #Get Customers Satisfaction Levels
            update_customer_satisfaction()


            #### UPDATE ####
            
            #Process Order
            #Check Ingredients --- OpenCV
            print("[LOG] Checking Quality of Ingredients")
            action = ir.recognize_ingredient()
                
            #Create Sandwich --- VREP
            print("[LOG] CREATING SANDWICH THEORETICALLY IN VREP")
            v.make_sandwich()

            #########################

                
            #Get Customers Satisfaction Levels
            pso_change = update_customer_satisfaction()
            
            #Log Order Completed and How Satisfactoraly
            f = open(base_dir + '\\machine_data.csv', 'w')
            data_logger = csv.writer(f)
            data = [customer_number, pso_change, order.get_order_value()]
            data_logger.writerow(data)
            f.close()
            
            print("[LOG] Process Complete. Restarting...")
            print("--------------------------------------------------")
            time.sleep(5)



def main():
    print_welcome()
    control_loop()
    
#Calling Main
if(__name__ == "__main__"):
    main()
