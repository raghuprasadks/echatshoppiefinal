from werkzeug.security import generate_password_hash

from user import User

from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

# Useful variables
serviceUsername = "d2469903-52e2-409b-8d78-8aca8e059214-bluemix"
servicePassword = "f3e87befbf58787bf72803e64abd7fb321a02ff2bcd031277ae7bd88f05dc6a0"
serviceURL = "https://d2469903-52e2-409b-8d78-8aca8e059214-bluemix:f3e87befbf58787bf72803e64abd7fb321a02ff2bcd031277ae7bd88f05dc6a0@d2469903-52e2-409b-8d78-8aca8e059214-bluemix.cloudantnosqldb.appdomain.cloud"

# This is the name of the database we are working with.
databaseName = "eshoppie"
print ("===\n")

# Use the IBM Cloudant library to create an IBM Cloudant client.
client = Cloudant(serviceUsername, servicePassword, url=serviceURL)

# Connect to the server
client.connect()

myDatabaseDemo = client.create_database(databaseName)

# Check that the database now exists.
if myDatabaseDemo.exists():
    print ("'{0}' successfully created.\n".format(databaseName))

# Space out the results.
print ("----\n")



def save_user(username, email,mobile,password):
    password_hash = generate_password_hash(password)
    #users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})
    isUserExists = False
    try:
        jsonDocument = {
            "name": username,
            "email": email,
            "mobile": mobile,
            "password": password_hash
        }
        
        print('get user :::',get_user(email))
        
        if(get_user(email)== None):
            print('User does not exists')
        
        # Create a document using the Database API.
            newDocument = myDatabaseDemo.create_document(jsonDocument)
        
        # Check that the document exists in the database.
            if newDocument.exists():
                print ("Document '{0}' successfully created.".format(email))
                print("Data committed")
        else:
            print('user  exits')
            isUserExists = True
    except Exception as e:
        print(e)
        return 'There was an issue in registering'
    return isUserExists

def get_user(email):
    #user_data = users_collection.find_one({'_id': username})
    print('get_user',email)
    user_data={};
    
    result_collection = Result(myDatabaseDemo.all_docs, include_docs=True)
    #result_collection = Result(myDatabaseDemo.all_docs)
    print ("Retrieved  document:",result_collection)
    print ("Retrieved minimal document:\n{0}\n".format(result_collection[0]))
    pasword_collection=''
    current_user={}
    isUserPresent=False
    for record in result_collection:
        print (record)
        print(type(record))
        print (' email value :get ::',record.get('doc').get('email'))
        doc=record.get('doc')
        
        if(doc.get('email')==email):
            pasword_collection=doc.get('password')
            user_data = doc
            isUserPresent=True
        
    #current_user = result_collection[reg_email]
    #print('user user : user name',user_data['name'])
    #current_user = Registration.find_by_email(reg_email)
    
    #if not isUserPresent:
        #return {'message': 'User {} doesn\'t exist'.format(username)}
         
        
    #return User(user_data['_id'], user_data['name'],user_data['mobile'],user_data['email'], user_data['password']) if user_data else None
    return User(user_data['name'],user_data['mobile'],user_data['email'], user_data['password']) if user_data else None

