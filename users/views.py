from django.shortcuts import render

from users.models import Staff, Student

# Create your views here.

def is_logged_in(request):
    return 'user' in request.session




def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        obj = Student.objects.filter( email = email, password = password )
        if not obj:
            obj = Staff.objects.filter( email = email, password = password )
        
        if not obj:
            return render( request, "users/login.html", {'message': 'No such user'} )
        obj = obj[0]
        
        request.session['user'] = { 'login_id': obj.id }
        return render( request, "users/login.html", {'message':'User logged in: '+str(obj.id) } )
            

    return render(request, "users/login.html")

def logout(request):
	request.session.flush()

	return render(request, "users/login.html", { 'message': 'Logged out' } )