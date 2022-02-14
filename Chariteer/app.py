#!/usr/bin/python
#import insert
import airtable
import os
import collections
import subprocess
from flask import Flask, redirect, url_for, render_template ,request, abort,session
#from retrieve import Ver_login 

app = Flask(__name__)
app.secret_key = "hello"

#import test_routes
myname='Guest'

@app.route("/")
def home():
	#print( 'myname:::' ,myname)
	if  "user" in session:
		myname = session["user"]
		UniID = session["UniID"]
		print( 'myname:::' ,myname)
	else:
		myname = 'Guest'
	return render_template("index.html",Disname=myname) 
	


@app.route("/index")
def index():
	if "user" in session:
		myname = session["user"]
		UniID = session["UniID"]
		print(UniID,myname)
		print(session)
	else:
		myname = 'Guest'
	print( 'myname:::' ,myname)
	return render_template("index.html",Disname=myname)

@app.route("/about")
def about():
	if "user" in session:
		myname = session["user"]
		UniID = session["UniID"]
		print(UniID,user)
	else:
		myname = 'Guest'
	return render_template("about.html", Disname = myname)
	


@app.route("/login", methods=["POST","GET"])
def login():
	if request.method == "POST":
		user = request.form["in_user"]
		password = request.form["in_pw"]
		#session["password"] = password
		res=Ver_login('Login',user,password)
		print('RES!!==',res)
		if res != 'FALSE' :
			myname=user
			UniID=res
			print('Name=',myname,'UniID=',UniID)
			session["user"] = user 
			session["UniID"] = UniID
			print (session)
			print ('session["user"]:' ,session["user"])
			print ('session["UniID"]:',session["UniID"])
			return redirect(url_for("home"))
			#return render_template("index.html",Disname=myname,DisID=UniID)
		else:
			#return f"<p>Irrcorrect username or password, Please try again</p>"
			return render_template("loginfailed.html")
	else:
		return render_template("login.html")


@app.route("/Usr<usr>", methods=["GET"])
def userhome(usr):
	retrieve()
	user = session["user"]
	UniID = session["UniID"]
	exe="grep \"{}\" ".format(usr) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"Organization_name\") print $(i+2)}' | cut -d \"'\" -f2"
	Org_Nm=os.popen(exe).read().split('\n')
	exe="grep \"{}\" ".format(usr) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"email\") print $(i+2)}' | cut -d \"'\" -f2"
	email=os.popen(exe).read().split('\n')
	exe="grep \"{}\" ".format(usr) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"Requirement\") print $(i+2)}' | cut -d \"'\" -f2"
	Skills=os.popen(exe).read().split('\n')
	exe="grep \"{}\" ".format(usr) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"First_name\") print $(i+2)}' | cut -d \"'\" -f2"
	First_Name=os.popen(exe).read().split('\n')
	exe="grep \"{}\" ".format(usr) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"Type\") print $(i+2)}' | cut -d \"'\" -f2"
	usrType=os.popen(exe).read().split('\n')
	return render_template("userProfileRO.html",Disname=user, Other_name=usr, DisID=UniID,Dis_First_Name=First_Name[0],Dis_Email=email[0],UsrType=usrType[0],Org_Name=Org_Nm[0],Skill=Skills[0])


@app.route("/user", methods=["POST","GET"])
def user():
	UniID = session["UniID"]
	#return f"<h1>Welcome! {usr}</h1>"
	if request.method == "GET":
		if "user" in session:
			user = session["user"]
			print(UniID,user)
			retrieve()
			exe="grep \"{}\" ".format(UniID) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"First_name\") print $(i+2)}' | cut -d \"'\" -f2"
			print("Exe:",exe)
			First_Name=os.popen(exe).read().split('\n')
			exe="grep \"{}\" ".format(UniID) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"email\") print $(i+2)}' | cut -d \"'\" -f2"
			email=os.popen(exe).read().split('\n')
			exe="grep \"{}\" ".format(UniID) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"Type\") print $(i+2)}' | cut -d \"'\" -f2"
			usrType=os.popen(exe).read().split('\n')
			exe="grep \"{}\" ".format(UniID) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"Organization_name\") print $(i+2)}' | cut -d \"'\" -f2"
			Org_Nm=os.popen(exe).read().split('\n')
			if usrType[0] == 'Type-0':
				exe="grep \"{}\" ".format(UniID) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"Requirement\") print $(i+2)}' | cut -d \"'\" -f2"
				Skills=os.popen(exe).read().split('\n')
			else:
				exe="grep \"{}\" ".format(UniID) +" b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"Skill\") print $(i+2)}' | cut -d \"'\" -f2"
				Skills=os.popen(exe).read().split('\n')
			print (user,'-',UniID,'-',First_Name[0],email[0],usrType[0])
			return render_template("userProfile.html",Disname=user,DisID=UniID,Dis_First_Name=First_Name[0],Dis_Email=email[0],UsrType=usrType[0],Org_Name=Org_Nm[0],Skill=Skills[0])

	if request.method == "POST":
		Updatedata={}
		if (request.form["in_pw"] != '****'):
			print("UP")
			NewUser= request.form["in_user"]
			session["user"] = NewUser
			NewPassword = request.form["in_pw"]
			NewFirstName = request.form["in_first_name"]
			NewEmail = request.form["in_email"]
			NewCharNm = request.form["in_charNum"]
			NewSkills = request.form["in_cb1"]+';'+request.form["in_cb2"] +';' +request.form["in_cb3"]+';'+ request.form["in_cb4"] + ';'+ request.form["in_cb5"] +';' + request.form["in_cb6"] +';' +request.form["in_cb7"]
			print('Skill:',NewSkills)
			if request.form["in_UsrType"] == 'Type-0':
				Updatedata = { "Username" : request.form["in_user"] ,
					"Password" : request.form["in_pw"],
					"Organization_name" : request.form["in_orgName"],
					"email" : request.form["in_email"],
					"Requirement": NewSkills,
					"registered_charity_number":request.form["in_charNum"]
					}
			else:
				Updatedata = { "Username" : request.form["in_user"] , 
					"Password" : request.form["in_pw"], 
					"First_name" : request.form["in_first_name"],
					"email" : request.form["in_email"],
					"Skill": NewSkills
					}
			
		else:
			NewUser= request.form["in_user"]
			NewFirstName = request.form["in_first_name"]
			NewCharNm = request.form["in_charNum"]
			session["user"] = NewUser
			print('test!!', NewFirstName)	
			NewEmail = request.form["in_email"]
			NewSkills = request.form["in_cb1"]+';'+request.form["in_cb2"] +';' +request.form["in_cb3"]+';'+ request.form["in_cb4"] + ';'+ request.form["in_cb5"] +';' + request.form["in_cb6"] +';' +request.form["in_cb7"]
			print('Skill:',request.form["in_UsrType"])
			myUsrType=request.form["in_UsrType"]	
			myorgNm=request.form["in_orgName"]
			print('Skill:',myUsrType)
			print( NewSkills.find("Communications and Marketing") )
			if request.form["in_UsrType"] == 'Type-0':
				Updatedata = { "Username" : request.form["in_user"] ,
					"Organization_name" : request.form["in_orgName"],
					"email" : request.form["in_email"],
					"Requirement": NewSkills,
					"registered_charity_number":request.form["in_charNum"]
					}
			else: 
				Updatedata = { "Username" : request.form["in_user"], 
					"First_name" : request.form["in_first_name"],
					"email" : request.form["in_email"],
					"Skill": NewSkills
					}
		print('Updatedata',Updatedata)
		at = airtable.Airtable('appaJ98wtnlFXGJed', 'keyD9PQvGAypUyIDG')
		at.update('Login',UniID,Updatedata)	
		#return f"<h1>Welcome! {usr}</h1>"
		return render_template("userProfile.html",Disname=NewUser,DisID=UniID,Dis_First_Name=NewFirstName,Update='Y',Dis_Email=NewEmail,UsrType=myUsrType,Org_Name=myorgNm,Skill=NewSkills,Dis_charNum=NewCharNm)




@app.route("/logout", methods=["POST","GET"])
def logout():
		session.pop("user",None)
		myname='Guest'
		print('Logout!', myname)
		return render_template("index.html",Disname=myname)



@app.route("/charity_registration",methods=["POST","GET"])
def charity_registration():
	if request.method == "POST":
		retrieve()
		user = request.form["in_user"]
		password = request.form["in_pw"]	
		email = request.form["in_email"]
		exe="cat b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"User_ID\") print $(i+1)}' | awk -F ',' '{print $2 }' |awk -F ')' '{print $1}' |sort -V | tail -n 1"
		print("Exe:",exe)
		UserID=os.popen(exe).read().split('\n')
		UsrID=int(UserID[0])+1
		print('Reg!:UserID',UsrID)
		data = {"Username":user,"Password":password,"email":email,"User_ID":UsrID,"Type":'Type-0'}
		at = airtable.Airtable('appaJ98wtnlFXGJed', 'keyD9PQvGAypUyIDG')
		res=Ver_login('Reg',user,password)
		print('Reg RES!!==',res)
		if (res == 'User Exists' ):
			#return "Username Exists, please try again"
			return render_template("charity_registration_userexist.html")
		else:
			at.create('Login', data)
			session["user"] = user
			res=Ver_login('Login',user,password)
			session["UniID"] = res 
			return render_template("index.html",Disname=user)
	else:
		return render_template("charity_registration.html")







@app.route("/volunteer_registration",methods=["POST","GET"])
def volunteer_registration():
	if request.method == "POST":
		retrieve()
		user = request.form["in_user"]
		password = request.form["in_pw"]
		email = request.form["in_email"]
		at = airtable.Airtable('appaJ98wtnlFXGJed', 'keyD9PQvGAypUyIDG')
		res=Ver_login('Reg',user,password)
		print('Reg RES!!==',res)
		exe="cat b.txt |awk -F \"'\" '{for(i=1;i<=NF;i++)if($i ~ \"User_ID\") print $(i+1)}' | awk -F ',' '{print $2 }' |awk -F ')' '{print $1}' |sort -V | tail -n 1"
		print("Exe:",exe)
		UserID=os.popen(exe).read().split('\n')
		UsrID=int(UserID[0])+1
		print('Reg!:UserID',UsrID)	
		data = {"Username":user,"Password":password,"email":email,"Type":'Type-1',"User_ID":UsrID}
		if (res == 'User Exists' ):
			#return "Username Exists, please try again"
			return render_template("volunteer_registration_userexist.html")
		else:
			at.create('Login', data)
			session["user"] = user
			res=Ver_login('Login',user,password)
			session["UniID"] = res
			return render_template("index.html",Disname=user)
	else:
		return render_template("volunteer_registration.html")



@app.route("/Register", methods=["POST","GET"])
def register():
	if request.method == "POST":
		user = request.form["in_user"]
		password = request.form["in_pw"]
		data = {"Username":user,"Password":password}
		at = airtable.Airtable('appaJ98wtnlFXGJed', 'keyD9PQvGAypUyIDG')
		#a=at.get('login',fields='Username')
		#print('A:', a)
		#print('Data:', data) 
		#print('-----------------')
		#python insert.py
		res=Ver_login('Reg',user,password)
		print('Reg RES!!==',res)
		if (res == 'User Exists' ):
			return "Username Exists, please try again"
		else: 
			at.create('Login', data)
			return f"<p>User {user} created</p>" 
	else:	
		return render_template("reg.html")


@app.route('/retrieve', methods=['GET'])
def Ver_login(z,x,y):
	at = airtable.Airtable('appaJ98wtnlFXGJed', 'keyD9PQvGAypUyIDG')
	a=at.get('login',fields='Username')
	#print(type(a))

	b=list(a)
	#print(type(b))

	od = collections.OrderedDict(sorted(a.items(), key=lambda x: x[1]))
	#print(od)
	#print('-------------')
	sorted_fruit_list = list(od.values())
	#print(len(sorted_fruit_list))

	str_1=' '.join(str(e) for e in sorted_fruit_list)
        #print(type(str))

	text_file = open("Output.txt", "w")
	text_file.write(str_1)
	text_file.close()

	exe="cat Output.txt| perl -pe 's/''createdTime/\\n/g' |  grep id | awk -F \"id\" '{print \"('\\''id\"$2}\' |sed \'s/].*$//g' >b.txt"
	print(exe)
	os.system(exe)

	f = open('b.txt')
	line=f.readline
	while line:
		print(line)
		#exe="echo \"{}\" |awk \'\{for(i=1;i<=NF;i++)if($i ~ \"Password\") print $(i+1)\}\' | cut -d \"'\" -f2".format(line)
		exe1="echo \"{}\" ".format(line)
		exe2="|awk '{for(i=1;i<=NF;i++)if($i ~ \"Username\") print $(i+1)}' | cut -d \"'\" -f2"
		exe3=exe1+" " + exe2
		#UsernameAAA=subprocess.check_output(exe3,shell=True)
		Username=os.popen(exe3).read().split('\n')
		print("User=",Username[0])
		if (z == 'Reg' and Username[0].upper() == x.upper()):
			return 'User Exists'

		if (z == 'Login' and Username[0].upper() == x.upper()):
			exe1="echo \"{}\" ".format(line)
			exe2="|awk '{for(i=1;i<=NF;i++)if($i ~ \"Password\") print $(i+1)}' | cut -d \"'\" -f2"
			exe3=exe1+" " + exe2
			Password=os.popen(exe3).read().split('\n')
			print("Password=",Password[0])
			exe1="echo \"{}\" ".format(line)
			exe2="|awk '{for(i=1;i<=NF;i++)if($i ~ \"id\") print $(i+1)}' | cut -d \"'\" -f2"
			exe3=exe1+" " + exe2
			UniID=os.popen(exe3).read().split('\n')			
			if (Password[0] == y):
				print ('Login success: ID=',UniID)
				return UniID[0]
			else:
				return 'FALSE'
		else:
			line=f.readline()
	f.close()
	return 'FALSE'


def Update(x,y):
	at = airtable.Airtable('appaJ98wtnlFXGJed', 'keyD9PQvGAypUyIDG')
	a=at.get('login',fields='Username')

	print(type(y))
	at.update('login',x,y)
	
def retrieve():
	at = airtable.Airtable('appaJ98wtnlFXGJed', 'keyD9PQvGAypUyIDG')
	a=at.get('login',fields='Username')
	b=list(a)
	#print(type(b))

	od = collections.OrderedDict(sorted(a.items(), key=lambda x: x[1]))
        #print(od)
        #print('-------------')
	sorted_fruit_list = list(od.values())
        #print(len(sorted_fruit_list))

	str_1=' '.join(str(e) for e in sorted_fruit_list)
        #print(type(str))

	text_file = open("Output.txt", "w")
	text_file.write(str_1)
	text_file.close()

	exe="cat Output.txt| perl -pe 's/''createdTime/\\n/g' |  grep id | awk -F \"id\" '{print \"('\\''id\"$2}\' |sed \'s/].*$//g' >b.txt"
	print(exe)
	os.system(exe)


def match(Skill):
	retrieve()
	

if __name__ == "__main__":
	app.run



#Update('recmX77hPvfgmECiJ',{"Username":"balamcld"})
#ID=Ver_login('Login','test','ates')
