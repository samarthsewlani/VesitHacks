from django.shortcuts import render,redirect
from vesit.models import Council_Student, Team_Student, Institute, Committee
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
        can_create = False
        add_to_council = False
        add_to_committee = False

        if type_user == 'student':
            can_create = can_create_event(obj)
            add_to_committee = check_add(obj,'committee')
            add_to_council = check_add(obj,'council')
        can_approve = check_approve(obj, type_user)
        
        print( f"create:{can_create} approve:{can_approve}  comm:{ add_to_committee} council: {add_to_council} " )

        request.session['user'] = { 'login_id': obj.id, 'type_user':type_user ,
        'can_create': can_create, 'can_approve':can_approve,
        'add_to_committee':add_to_committee, 'add_to_council':add_to_council }
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
    fields=['name','email','gender','iid','mobile_num','image','dept']

    def form_valid(self,form):
        print(self.request.POST)
        form.instance.password=self.request.POST.get("pass")
        return super().form_valid(form)


class StudentListView(ListView):
    model = Student
    template_name = "users/student_list.html"
    context_object_name="students"
    paginate_by=7
    
    

class StudentDetailView(DetailView):
    model = Student
    template_name = "users/student_detail.html"
    context_object_name="student"


def can_create_event(user):
    cs = Council_Student.objects.filter(student_type = 'S', student=user)
    if not cs:
        cs = Team_Student.objects.filter(student_type = 'H', student=user)
    if cs:
        return True
    return False


def check_approve(user, type_user):

    if type_user =='student':
        ins_obj = Institute.objects.filter(gs = user)
        if ins_obj:
            return True
        else:
            comm = Committee.objects.filter(chair_person=user)
            if comm:
                return True
    else:
        ins_obj = Institute.objects.filter(principal = user)
        if ins_obj:
            return True
        else:
            comm = Committee.objects.filter(faculty_head1=user)
            if comm:
                return True
            else:
                if user.staff_type == 'H':
                    return True
    return False


def check_add(user, type_team):
    if type_team == 'committee':
        cp = Committee.objects.filter(chair_person = user)
        if cp:
            return True
    else:
        cs = Council_Student.objects.filter(student_type = 'S', student=user)
        if cs:
            return True
    return False
