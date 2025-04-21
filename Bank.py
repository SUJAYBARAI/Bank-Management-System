from pathlib import Path
import json
import random
import string
import streamlit as st


class Bank:
    __database = "data.json"
    data = []

    try:
        if Path(__database).exists():
            with open(__database) as fs:
                data = json.loads(fs.read())
    except Exception as err:
        print(f"An error occured as {err}")
    
    @classmethod
    def Update_data(cls):
        with open(cls.__database,'w') as fs:
            fs.write(json.dumps(cls.data))
    
    @classmethod
    def Generate_Account(cls):
        alpha = random.choices(string.ascii_letters,k = 4)
        numbers = random.choices(string.digits,k = 8)
        id = alpha + numbers
        random.shuffle(id)
        return "".join(id)
        
    def createuser(self,name,email,age,phonenumber,pin):
        info = {
            "name":name,
            "email":email,
            "age":age,
            "phonenumber":phonenumber,
            "pin":pin,
            "AccountNo.":Bank.Generate_Account(),
            "balance":0
        }
        
        if info["age"] < 18:
            print("sorry you can't create an account at this age 💀")
        
        elif (not len(str(info["phonenumber"])) == 10) or (not len(str(info["pin"])) == 4):
            print("invalid input please try again")
        
        else:
            print(f"\n\n\nplease keep your account number safe\n   your account number is\n       {info["AccountNo."]}")
            Bank.data.append(info)
            Bank.Update_data()
    
    def Deposit_money(self,accountno,pin,amount):
        # AC = input("please tell your account number")
        # pin = int(input("please tell your pin"))

        # for i in Bank.data:
        #     if i["AccountNo."] == AC and i['pin'] == pin:
        #         userdata = i
        #         break
        # else:
        #     print("sorry no data found please recheck your A.C number and pin")
        # amount=amount
        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]
        if user_data == False:
            print("sorry no data found please check your credentials.")
        else:
            amount = amount
            if amount <= 0:
                print("your deposit money should not be less than 0")
            elif amount > 100000000:
                print("sorry you cannot deposit more that 10000")
            else:
                user_data[0]["balance"] += amount
                Bank.Update_data()
                print("Balance deposited successfully.")

    def Withdraw_money(self,accountno,pin,amount):
        # AC = input("please tell your account number")
        # pin = int(input("please tell your pin"))
        
        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]
        if user_data == False:
            print("sorry no data found please check your credentials.")
        else:
            amount = amount
            if amount <= 0:
                print("your withdrawal money should not be less than 0")
            elif amount > 100000000:
                print("sorry you cannot withdraw more that 10000")
            else:
                if user_data[0]["balance"] < amount:
                    print("sorry insufficient balance.")
                else:
                    user_data[0]["balance"] -= amount
                    Bank.Update_data()
                    print("withdrawl successfull.")

    def details(self,accountno,pin):
        # AC = input("please tell your account number")
        # pin = int(input("please tell your pin"))

        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]

        if user_data == False:
            print("sorry no data found please check your credentials.")
        else:
            print("your details are : ")
            for i in user_data[0]:
                st.write(f"{i} : {user_data[0][i]} ")
    
    def update_details(self,accountno,pin):
        # AC = input("please tell your account number")
        # pin = int(input("please tell your pin"))

        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]

        if user_data == False:
                print("sorry no data found please check your credentials.")
        
        else:
            print("you cannot change the Account No.")
            print("now update your details or skip it by just pressing enter")

            newdata = {
                "name":input("Update your name or press enter to skip"),
                "age":input("update your age or press enter to skip"),
                "email":input("update your email or press enter to skip"),
                "phonenumber":input("update your phonenumber or press enter to skip"),
                "pin":input("update your pin or press enter to skip")
            }
        
            if newdata["name"] == "":
                newdata["name"] = user_data[0]["name"]
            if newdata["age"] == "":
                newdata["age"] = user_data[0]["age"]
            if newdata["email"] == "":
                newdata["email"] = user_data[0]["email"]
            if newdata["phonenumber"] == "":
                newdata["phonenumber"] = user_data[0]["phonenumber"]
            if newdata["pin"] == "":
                newdata["pin"] = user_data[0]["pin"]
            
            newdata["AccountNo."] = user_data[0]["AccountNo."]
            newdata["balance"] = user_data[0]["balance"]

            
            for i in user_data[0]:
                if user_data[0][i] == newdata[i]:
                    continue
                else:
                    if newdata[i].isnumeric():
                        user_data[0][i] = int(newdata[i])
                    else:
                        user_data[0][i] = newdata[i]


            Bank.Update_data()
            print("details updated successfully")
    

    def Delete_user(self,accountno,pin):
        # AC = input("please tell your account number")
        # pin = int(input("please tell your pin"))

        user_data = [i for i in Bank.data if i["AccountNo."] == accountno and i["pin"] == pin]
        if not user_data:
            return "Account not found or invalid credentials"
        else:
            Bank.data.remove(user_data[0])
            Bank.Update_data()
            return "Account deleted successfully"

        
            


# streamlit parts

st.title("Royal Bank")
bank = Bank()
menu=["Create Account","Deposite Money","Withdraw Money","View Details","Update Details","Delete User"]
choices=st.sidebar.selectbox("Select here",menu)

if choices=="Create Account":
    # st.write("Welcome to Create Account page")
    st.subheader("Create Account")
    name=st.text_input("Enter Your Name")
    email=st.text_input("Enter Your Email id")
    age=st.number_input("Enter Your Age",min_value=0,step=1)
    phonenumber=st.text_input("Enter Your PhoneNumber")
    pin=st.text_input("Enter Your Pin",type="password")

    if st.button("Create Account"):
        if name and email and age and phonenumber and pin:
            response=bank.createuser(name,email,age,int(phonenumber),int(pin))
            st.success("Congratulation your account created")
        else:
            st.error("Invalid input")

if choices=="Deposite Money":
#   st.write("Welcome to Deposite Money page")
    st.subheader("Deposite Money")
    accountno=st.text_input("Enter Your  Account Number")
    pin=st.text_input("Enter Your Pin",type="password")
    amount=st.number_input("Enter Your amount",min_value=0,step=1)
    
    if st.button("Deposite"):
        if accountno and pin and amount:
            result=bank.Deposit_money(accountno,int(pin),int(amount))
            st.success("Congratulation your money deposited")
        else:
            st.error("Invalid input")

if choices=="Withdraw Money":
#     st.write("Welcome to Withdraw Money page")
    st.subheader("Withdraw  Money")
    accountno=st.text_input("Please enter your  Account Number")
    pin=st.text_input("Enter Your Pin",type="password")
    amount=st.number_input("Enter Your amount",min_value=0,step=1)
    if st.button("Withdraw"):
        if accountno and pin and amount:
            response=bank.Withdraw_money(accountno,int(pin),amount)
            st.success("Withdrawal successful")
        else:
            st.error("Invalid Inputs")


if choices=="View Details":
#     st.write("Welcome to View Details page")
    st.subheader("View Details")
    accountno=st.text_input("Please enter your  Account Number")
    pin=st.text_input("Enter Your Pin",type="password")
    if st.button("View Details"):
        if accountno and pin:
            response=bank.details(accountno,int(pin))
            st.success("Successfully")
        else:
            st.error("Invalid Inputs")
            

if choices=="Update Details":
    def update_details():
        st.title("Update Your Account Details")

    account_no = st.text_input("Enter your account number:")
    pin = st.text_input("Enter your PIN:", type="password")

    if st.button("Submit"):
        user_data = [i for i in Bank.data if i["AccountNo."] == account_no and i["pin"] == int(pin)]

        if not user_data:
            st.error("Sorry, no data found. Please check your credentials.")
        else:
            st.success("Credentials verified. You can now update your details.")

            user = user_data[0]

            # Input fields for updating user details
            new_name = st.text_input("Update your name", value=user["name"])
            new_age = st.text_input("Update your age", value=user["age"])
            new_email = st.text_input("Update your email", value=user["email"])
            new_phonenumber = st.text_input("Update your phone number", value=user["phonenumber"])
            new_pin = st.text_input("Update your PIN", value=str(user["pin"]), type="password")

            if st.button("Update Details"):
                updated_data = {
                    "name": new_name or user["name"],
                    "age": new_age or user["age"],
                    "email": new_email or user["email"],
                    "phonenumber": new_phonenumber or user["phonenumber"],
                    "pin": int(new_pin) if new_pin else user["pin"],
                    "AccountNo.": user["AccountNo."]
                }

                user.update(updated_data)
                Bank.Update_data()
                st.success("Details updated successfully!")


if choices=="Delete User":
    st.subheader("Delete User")
    accountno=st.text_input("Please enter your  Account Number")
    pin=st.text_input("Enter Your Pin",type="password")
    if st.button("Delete User"):
        response=bank.Delete_user(accountno,int(pin))
        if "successfully" in response:
            st.success("Successfully")
        else:
            st.error(response)


    