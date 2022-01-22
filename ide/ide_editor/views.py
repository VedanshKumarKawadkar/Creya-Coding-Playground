from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from inflection import re
from json import dumps
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
    return render(request, "editor.html")


def runCode(request):
    if request.method == "POST":
        id_api = "https://ide.geeksforgeeks.org/main.php"
        output_api = "https://ide.geeksforgeeks.org/submissionResult.php"

        code = request.POST.get("code")
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
        id_api_response = requests.post(id_api, data=id_api_data).json()

        sid = id_api_response['sid']
        print(sid)

        status = "IN-QUEUE"
        while(status != "SUCCESS"):
            output_api_response = requests.post(output_api, data={'sid':sid, 'requestType':'fetchResults'}).json()
            status = output_api_response['status']
            print(output_api_response)

        output = ""
        memory = ""
        runtime = ""

        print(output_api_response)

        if(output_api_response['compResult']=='F'):
            ...
        
        elif(output_api_response['compResult']=='S'):
            if('rntError' in output_api_response):
                print(output_api_response['rntError'])
                output = output_api_response['rntError']
                runtime = output_api_response['time']
                memory = output_api_response['memory']

            elif('output' in output_api_response):
                print(output_api_response['output'])
                output = output_api_response['output']
                runtime = output_api_response['time']
                memory = output_api_response['memory']

            elif('output' not in output_api_response):
                print("No output")
                output = "No Output"
                runtime = output_api_response['time']
                memory = output_api_response['memory']

        output_data = [{"code":code, "input":inputs, "output":output, "runtime":runtime, "memory":memory}]
        output_json = {"code":code, "input":inputs, "output":output, "runtime":runtime, "memory":memory}
        print(output_data)
        context = {"data": output_data}
        return JsonResponse(output_json)
        #return render(request, "editor.html", context=context)
    

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']
        user = request.POST['username']
        print(user, pwd, email)

        client = MongoClient(host=client_string, connect=False)
        ideDB = client.ide
        user_details_coll = ideDB.user_details

        user_details_coll.insert_one({
            "username":user,
            "email":email,
            "password":pwd,
            "hashed_pwd": bcrypt.hashpw(pwd, salt=bcrypt.gensalt(rounds=8))
        })

        return HttpResponse("")
