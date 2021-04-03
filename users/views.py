from django.shortcuts import render,redirect

from users.models import Staff, Student
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Staff, Student, Department
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

# Create your views here.
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.contrib.auth.views import redirect_to_login

def is_logged_in(request):
    return 'user' in request.session




def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        type_user=''

        obj = Student.objects.filter( email = email, password = password )
        type_user = 'student'
        if not obj:
            obj = Staff.objects.filter( email = email, password = password )
            type_user = 'staff'
        
        if not obj:
            return render( request, "users/login.html", {'message': 'No such user'} )
        obj = obj[0]
        request.session['user'] = { 'login_id': obj.id, 'type_user':type_user }
        #print("\n\nsession", request.__dict__)
        return render( request, "users/login.html", {'message':'User logged in: '+str(obj.id) } )
            

    return render(request, "users/login.html")

def logout(request):
	request.session.flush()

	return render(request, "users/logout.html", { 'message': 'Logged out' } )

class DepartmentCreateView(LoginRequiredMixin,CreateView):
    model = Department
    template_name = "users/new_department.html"
    fields=["name"]

    def handle_no_permission(self):
        if self.raise_exception or is_logged_in(self.request):
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('login')

class DepartmentListView(ListView):
    model = Department
    template_name = "users/department_list.html"
    context_object_name="departments"
    

class DepartmentDetailView(DetailView):
    model = Department
    template_name = "users/department_detail.html"
    context_object_name="department"

class StudentCreateView(CreateView):
    model = Student
    template_name = "users/new_student.html"
    fields=['name','email','gender','iid','mobile_num','image','dept','password']


class StudentListView(ListView):
    model = Student
    template_name = "users/student_list.html"
    context_object_name="students"
    paginate_by=7
    
    

class StudentDetailView(DetailView):
    model = Student
    template_name = "users/student_detail.html"
    context_object_name="student"