from django.db import models

# Section model: just the title and prefix
class Section(models.Model):
    prefix = models.CharField(max_length=1, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.prefix}. {self.title}"

# Question (SectionItem) model: linked to Section
class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField()  # order in the section
    text = models.TextField()

    class Meta:
        unique_together = ('section', 'order')
        ordering = ['section__prefix', 'order']

    def __str__(self):
        return f"{self.section.prefix}{self.order}. {self.text[:50]}..."
    
# Subject model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    
# Course model
class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

# Teacher model
class Teacher(models.Model):
    first_name = models.CharField(max_length=50,null=True, blank=True)
    last_name = models.CharField(max_length=50,null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class TeacherEvaluation(models.Model):
    teacher = models.ForeignKey(
        'Teacher', 
        on_delete=models.CASCADE, 
        related_name='evaluations'
    )
    student_id = models.CharField(max_length=50)  # Anonymous student identifier
    student_name = models.CharField(max_length=100, null=True,blank=True)  # Optional student name

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        'Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    semester = models.CharField(max_length=20, blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    year_level = models.CharField(max_length=10, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # ⭐ NEW FIELD
    overall_rating = models.FloatField(null=True, blank=True)
    
    commendable_features = models.TextField(blank=True, null=True)
    suggestions_improvement = models.TextField(blank=True, null=True)

    class Meta:
        # Prevent multiple entries for the same teacher, student, subject, semester, and academic year
        unique_together = ('teacher', 'student_id', 'subject', 'semester', 'academic_year')

   
    @property
    def overall_computed_rating(self):
        ratings = []
        for item in self.items.all():
            try:
                ratings.append(float(item.rating))
            except (ValueError, TypeError):
                continue
        if ratings:
            return round(sum(ratings)/len(ratings), 2)
        return None

# EvaluationItem: stores rating per question for a given evaluation
class EvaluationItem(models.Model):
    evaluation = models.ForeignKey(TeacherEvaluation, on_delete=models.CASCADE, related_name="items")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rating = models.CharField(
        max_length=2,
        choices=[
            ('5', 'Outstanding'),
            ('4', 'Good'),
            ('3', 'Average'),
            ('2', 'Needs Improvement'),
            ('1', 'Unsatisfactory'),
            ('N', 'Not Observed')
        ]
    )

    def __str__(self):
        return f"{self.question.section.prefix}{self.question.order} - {self.rating}"


class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.student_id
