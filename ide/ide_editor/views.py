from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from json import dumps
from pydantic import Json
from ide_editor.models import CodeData
import requests
import time
from pymongo import MongoClient
import bcrypt

# Create your views here.
client_string = "mongodb+srv://vk:1234@ide.gt9wy.mongodb.net/ide?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

def home(request):
    return render(request, "login-signup.html")


def editor(request):
    username = request.session["username"]
    email = request.session["email"]
    print(username, email)
    data = [{"username":username, "email":email}]
    context = {"data":data}
    return render(request, "question_editor.html", context=context)


def runCode(request):
    if request.method == "POST":
        id_api = "https://ide.geeksforgeeks.org/main.php"
        output_api = "https://ide.geeksforgeeks.org/submissionResult.php"

        code = request.POST.get("code")
        print(code)
        if(code==""):
            code = " "
        lang = request.POST["lang"]
        inputs = request.POST["input"]
        #theme = request.POST["theme"]

        lang_dict = {"python":'Python3', "c_cpp":'Cpp14', "java":'Java', "c_cpp2":'C'}
        language = lang_dict[lang]
        save = False
        
        id_api_data = {
            "lang" : language,
            "code" : code,
            "input": inputs,
            "save" : save
        }
        print(id_api_data)
        id_api_response = requests.post(id_api, data=id_api_data).json()

        sid = id_api_response['sid']
        #print(sid)

        status = "IN-QUEUE"
        while(status != "SUCCESS"):
            output_api_response = requests.post(output_api, data={'sid':sid, 'requestType':'fetchResults'}).json()
            status = output_api_response['status']
            #print(output_api_response)

        output = ""
        memory = ""
        runtime = ""

        print(output_api_response)

        if(output_api_response['compResult']=='F'):
            output = output_api_response['cmpError']
            #runtime = output_api_response['runtime']
            #memory = output_api_response['memory']
        
        elif(output_api_response['compResult']=='S'):
            if('rntError' in output_api_response):
                #print(output_api_response['rntError'])
                output = output_api_response['rntError']
                runtime = output_api_response['time']
                memory = output_api_response['memory']

            elif('output' in output_api_response):
                #print(output_api_response['output'])
                output = output_api_response['output']
                runtime = output_api_response['time']
                memory = output_api_response['memory']

            elif('output' not in output_api_response):
                #print("No output")
                output = "No Output"
                runtime = output_api_response['time']
                memory = output_api_response['memory']

        output_data = [{"code":code, "input":inputs, "output":output, "runtime":runtime, "memory":memory}]
        output_json = {"code":code, "input":inputs, "output":output, "runtime":runtime, "memory":memory}
        print(output_data)
        context = {"data": output_data}
        return JsonResponse(output_json)
       
    
def login(request):
    if(request.method == "POST"):
        email = request.POST['login_email']
        pwd = request.POST['login_password']
        client = MongoClient(host=client_string, connect=False)
        ideDB = client.ide
        user_details_coll = ideDB.user_details

        check_email = user_details_coll.find_one({"email":email})
        print(check_email)
        if(check_email):
            pwd2 = check_email['password']
            print(pwd2)
            if(pwd == pwd2):
                request.session["username"] = check_email["username"]
                request.session["email"] = check_email["email"]
                return render(request, "question_editor.html")
            else:
                msg = "Password is incorrect."
                return JsonResponse({"msg":msg})
        else:
            msg = "Email does not exist."
            return JsonResponse({"msg":msg})
        

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('signup_email')
        pwd = request.POST.get('signup_password')
        pwd = str(pwd)
        username = request.POST.get('signup_username')
        re_pwd = request.POST.get('signup_password_confirm')
        print(username, pwd, email, re_pwd)

        client = MongoClient(host=client_string, connect=False)
        ideDB = client.ide
        user_details_coll = ideDB.user_details

        check_email = user_details_coll.find_one({"email":email})
        print(check_email)
        check_username = user_details_coll.find_one({"username":username})
        print(check_username)

        if(check_email!=None):
            msg = "E-mail already present."
            message = {"message":msg}
            return JsonResponse(message)
        
        elif check_email==None and check_username!=None:
            msg = "Username already exists."
            message = {"message":msg}
            return JsonResponse(message)

        elif check_email == None and check_username==None:
            user_details = {
                "username":username,
                "email":email,
                "password":pwd,
                "hashed_pwd": bcrypt.hashpw(pwd.encode('utf-8'), salt=bcrypt.gensalt(rounds=8))
            }
            user_details_coll.insert_one(user_details)
            msg = "New User Created."
            message = {"message":msg}
            return JsonResponse(message)


def logout(request):
    if request.method == "POST":
        email = request.session["email"]
        username = request.session["username"]
        del email
        del username

        return redirect("/login")