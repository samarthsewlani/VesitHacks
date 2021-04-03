from django.shortcuts import render, redirect
from .models import Event, Council, Council_Student, Team_Student, Institute,Committee, Dept_Allowed
from users.models import Student,Staff
from django import forms
from django.views.generic import CreateView, ListView , DetailView
# Create your views here.
from .forms import EventCreateForm, DateForm
import datetime
from users.views import is_logged_in
from django.db.models.query import QuerySet

def home(request):
    events=Event.objects.filter(is_approved2=True,is_approved1=True,event_type='I')
    return render( request, 'vesit/home.html' ,{'events':events})


class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','description','start_time','end_time','event_type']

def index(request):
    event_form=EventForm()
    return render(request, 'vesit/index.html',{'event_form':event_form})


def create_event(request):
    if is_logged_in(request):
        if request.method == "POST":
            date = request.POST['start_date']
            start_date = datetime.datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
            date = request.POST['end_date']
            end_date = datetime.datetime.strptime(date, '%m/%d/%Y %I:%M:%S %p')
            name = request.POST['name']
            description = request.POST['description']
            event_type = request.POST['event_type']
            location = request.POST['location']


            sid = request.session['user']['login_id'] 
            stu =Student.objects.filter(id = sid)[0]
            event = Event( name = name, description = description,
            start_time = start_date, end_time=end_date,
            event_type=event_type, location=location,
            submitted_by=stu  )
            council_student = Council_Student.objects.filter( student = stu )
            if council_student:
                council_student = council_student[0]
                print("CS:",council_student)
                event.council = council_student.council
                
            
            committe_student = Team_Student.objects.filter(id = sid)
            if committe_student:
                committe_student=committe_student[0]
                event.committee = committe_student.team.committee
            
            print(event)
            
            event.save()
        return render(request, 'vesit/create_event.html', {'form': DateForm(), 'event_form': EventCreateForm })
    else:
        return redirect('login')

def event(request):
    events=Event.objects.filter(is_approved2=True,is_approved1=True, event_type='I')
    if is_logged_in(request):
        
        user = None
        user_id = request.session['user']['login_id']
        if request.session['user']['type_user']=='student':
            user = Student.objects.filter(id = user_id)[0]
        else:
            user = Staff.objects.filter(id = user_id)[0]
        
        dpt_allowed = Dept_Allowed.objects.filter(dept_id=user.dept, is_approved=True)
        dept_events = QuerySet()
        if dpt_allowed:
            eids = []
            for d in dpt_allowed:
                eids.append(d.event_id.id)
            print("eids",eids)
            dept_events = Event.objects.filter(id__in=eids)
            if dept_events:
                events = events.union(dept_events)
    return render(request, 'vesit/events.html',{'events':events })



class EventDetailView(DetailView):
    model = Event
    template_name = "vesit/event_detail.html"
    context_object_name = "event"

def approve_events(request):
    if is_logged_in(request):
        level = 1
        user_id = request.session['user']['login_id']
        type_user = request.session['user']['type_user']
        if type_user == 'student':
            user = Student.objects.filter(id = user_id)
        else:
            user = Staff.objects.filter(id = user_id)

        if not user:
            return redirect('home')
        
        user=user[0]
        events = None
        ins_obj = Institute.objects.all()[0]
        GS = ins_obj.gs
        Principal = ins_obj.principal

        
        if type_user == 'student':
            #for GS
            if user == GS:
                events = Event.objects.filter( council__isnull=False, is_approved1=None )
            else:    
                committe = Committee.objects.filter(chair_person = user)

                #for chair person 
                if committe:
                    committe=committe[0]
                    events = Event.objects.filter( committee=committe, is_approved1=None )
        else:
            level = 2
            #print("2\n\n\newrfuyefrhr")
            if user == Principal:
                level = 2
                events = Event.objects.filter( council__isnull=False, is_approved1=True, is_approved2=None )
            else:
                # for faculty head
                committe = Committee.objects.filter(faculty_head1=user)
                if committe:
                    committe=committe[0]
                    level=2
                    events = Event.objects.filter( committee=committe, is_approved1=True, is_approved2=None )
                else:
                    #for HOD
                    level = 3
                    dept = user.dept
                    if user.staff_type =='H':
                        event_ids = Dept_Allowed.objects.filter( dept_id=dept )
                        
                        eids = []
                        for e in event_ids:
                            eids.append(e.event_id.id)
                        
                        events = Event.objects.filter(id__in=eids, is_approved1=True, is_approved2=True)
        return render(request, "vesit/approve_events.html", { 'events': events, 'level':level } )   
    return redirect('login')


def approve_level(request, eid,  approved, level):
    dct = {1:True, 0: False}
    approved = dct[approved]
    event = Event.objects.filter(id = eid)
    if event:
        event = event[0]
        if level == 1:
            event.is_approved1 = approved
            event.save()
        elif level==2:
            event.is_approved2 = approved
            event.save()
        elif level==3:
            uid = request.session['user']['login_id']
            user = Staff.objects.filter(id = uid  )
            dpt_allowed = Dept_Allowed(event_id= event, dept_id= user.dept)
            dpt_allowed.is_approved = approved
            dpt_allowed.save()
    return redirect('approve_events')

def approve_event_detail(request,event_id,level):
    event=Event.objects.filter(id=event_id).first()
    return render(request,'vesit/event_approve_detail.html',{'event':event,'level':level})
        

class CouncilStudentCreateView(CreateView):
    model = Council_Student
    template_name = "vesit/council_student_create.html"
    fields =['council','student','student_type']


class CouncilStudentListView(ListView):
    model = Council_Student
    template_name = "vesit/council_student_list.html"
    context_object_name = "council_students"
    paginate_by=7

class CouncilStudentDetailView(DetailView):
    model = Council_Student
    template_name = "vesit/council_student_detail.html"
    context_object_name = "council_student"
    

class TeamStudentCreateView(CreateView):
    model = Team_Student
    template_name = "vesit/team_student_create.html"
    fields =['team','student','student_type']

class TeamStudentListView(ListView):
    model = Team_Student
    template_name = "vesit/team_student_list.html"
    context_object_name = "team_students"
    paginate_by=7

class TeamStudentDetailView(DetailView):
    model = Team_Student
    template_name = "vesit/team_student_detail.html"
    context_object_name = "team_student"


