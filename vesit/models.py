from django.db import models
from users.models import Student,Staff, Department
from django.urls import reverse

# Create your models here.


class Institute(models.Model):
    principal = models.ForeignKey(Staff, on_delete = models.CASCADE)
    gs = models.ForeignKey(Student, on_delete = models.CASCADE)

    def __str__(self):
        return "Principal: "+self.principal.name + " ,GS: "+self.gs.name


class Council(models.Model):
    name = models.CharField( max_length= 100 )

    def __str__(self):
        return "Council: " + self.name

class Council_Student(models.Model):
    council = models.ForeignKey(Council, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    COUNCIL_CHOICES = (
        ('S', 'Secratary'),
        ('I', 'Incharge'),
        
    )
    student_type = models.CharField(max_length=1, choices=COUNCIL_CHOICES)

    def __str__(self):
        return "Council: " + self.council.name + " , " + self.student_type + " : " + self.student.name
    
    def get_absolute_url(self):
        return reverse('council_student_detail', kwargs={'pk': self.pk})




class Committee(models.Model):
    name =  models.CharField( max_length= 100 )
    chair_person = models.ForeignKey(Student, on_delete = models.CASCADE)
    treasurer = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = 'treasurer')
    ceo = models.ForeignKey(Student, on_delete = models.CASCADE, related_name= 'ceo')
    faculty_head1 = models.ForeignKey(Staff, on_delete = models.CASCADE)
    faculty_head2= models.ForeignKey(Staff, on_delete = models.CASCADE, null = True, related_name= 'faculty_head2')

    def __str__(self):
        return "Committe: "+ self.name

class Team(models.Model):
    name = models.CharField( max_length= 100 )
    committee = models.ForeignKey(Committee, on_delete = models.CASCADE)

    def __str__(self):
        return "Committee: "+self.committee.name + " ,Team: "+self.name

    
    

class Team_Student(models.Model):
    team = models.ForeignKey(Team, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    choices = (
        ('H', 'Head'),
        ('I', 'Incharge'),
    )
    student_type = models.CharField(max_length=1, choices=choices)

    def __str__(self):
        return "Committe: "+ self.team.committee.name + " , "+ self.student_type + " : "+ self.student.name
    
    def get_absolute_url(self):
        return reverse('team_student_detail', kwargs={'pk': self.pk})


class Event(models.Model):
    name = models.CharField( max_length= 100 )
    description = models.TextField( max_length= 100 )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    choices = (
        ('D', 'Department Level'),
        ('I', 'Institute Level'),
    )
    event_type = models.CharField(max_length=1, choices=choices)
    location = models.CharField( max_length=100 )
    council = models.ForeignKey( Council , on_delete=models.CASCADE, null = True, blank =True)
    committee = models.ForeignKey( Committee , on_delete=models.CASCADE, null = True, blank =True)
    submitted_by = models.ForeignKey( Student, on_delete=models.CASCADE)
    is_approved1 = models.BooleanField(null = True, default=None)
    is_approved2 = models.BooleanField(null = True, default=None)

    def __str__(self):
        string  = self.name+" , Organized by: "
        if self.council:
            string+= self.council.name+ " Council"

        if self.committee:
            string+= self.committee.name + " Committe"
        return  string

class Dept_Allowed(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_approved = models.BooleanField( null = True, default=None )
