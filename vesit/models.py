from django.db import models
from users.models import Student,Staff

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