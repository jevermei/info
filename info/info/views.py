from django.shortcuts import render, redirect
from info.models import User, Line, Stop, Report

def login_view(request):
    if 'email' in request.GET and 'password' in request.GET:
        enteredEmail = request.GET['email']
        enteredPassword = request.GET['password']
        if len(User.objects.filter(email=enteredEmail).filter(password=enteredPassword)) == 1:
            user_loggedin = User.objects.get(email = enteredEmail)
            request.session['email'] = user_loggedin.email
            return redirect('/welcome')
        else: 
            template_values = {'error' : 'Mauvaise adresse email ou mauvais mdp'}
            return render(request,'login.html',template_values)
    else:
        return render(request, 'login.html')

def welcome_view(request):
    if "email" in request.session:
        user = User.objects.get(email = request.session['email'])
        lines = Line.objects.all() 
        
        if User.objects.filter(email = request.session['email']).filter(admin = True ):
            template_values ={'admin':"You are an admin",'line': lines}
            response = render (request,'welcome.html',template_values)
        else :
            template_values ={'erroradmin':"You are not an admin",'line':lines}
            response = render (request,'welcome.html',template_values)
    else:
        response = redirect('/login')
    return response

def register_view(request):
    if 'firstname' in request.GET:
        newUser = User (firstname = request.GET['firstname'], 
                        lastname = request.GET['lastname'],
                        email = request.GET['email'],
                        admin = request.GET['admin'],
                        password = request.GET['password']
                        )
        newUser.save()
        return redirect('/login')
    else :
        return render(request, 'register.html')

def network_view(request):
    if "email" in request.session:
        if User.objects.filter(admin = True ):
            if "line_number" in request.GET:
                newline = Line(line_number= request.GET["line_number"])
                newline.save()
                lines = Line.objects.all()
                stops = Stop.objects.all()
                template_values ={'line': lines,'stops': stops}
                response = render (request,'network.html',template_values)
            else:
                lines = Line.objects.all()
                stops = Stop.objects.all()
                template_values ={'line': lines, 'stops': stops, 'empty': 'veillez remplir les champs vides'}
                response = render (request,'network.html',template_values)
        else:
            response = redirect('/welcome')
    else:
        response = redirect('/login')

    return response 

def stop_view(request):
    if "email" in request.session:
        if User.objects.filter(admin = True):
            if 'stopname' in request.GET:
                lines = Line.objects.all()
                stops = Stop.objects.all()
                newStop = Stop(
                    stopname = request.GET['stopname'],
                    order = 100,
                    stop_line = Line.objects.get(line_number = request.GET["lineNr"])
                    
                )
                newStop.save() 
                template_values ={'line': lines, 'stops': stops}
                response = render (request,'stop.html',template_values)
            else:
                lines = Line.objects.all()
                stops = Stop.objects.all()
                template_values ={'line': lines, 'stops': stops, 'empty': 'veuillez remplir les champs vides'}
                response = render (request,'stop.html',template_values)
        else:
            response = redirect('/welcome')
    else:
        response = redirect('/login')
    return response

def report_view(request):
    if "email" in request.session:
        if 'reportstop' in request.GET:
            user = User.objects.get(email = request.session['email'])
            reportline = Line.objects.get(line_number = request.GET["reportline"])
            reportstop = Stop.objects.get(stopname = request.GET["reportstop"])
            new_report = Report(user = user,
                                reportstop = reportstop,
                                reportline = reportline)
            new_report.save()
            lines = Line.objects.all()
            stops = Stop.objects.all()
            template_values = {'line': lines,'stops': stops,"thanks" : "thanks for your report"}
            response = render(request, 'report.html', template_values) 
        else:
            lines = Line.objects.all()
            stops = Stop.objects.all()
            template_values = {'line': lines,'stops': stops}
            response = render(request, 'report.html',template_values)
    else:
        response = redirect('/login')
    return response



