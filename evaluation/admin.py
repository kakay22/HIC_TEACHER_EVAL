from django.contrib import admin
from .models import Section, Question, Teacher, Course, Subject, TeacherEvaluation, EvaluationItem, Student

# Inline to add questions inside Section
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # allows adding one extra question at a time
    fields = ['order', 'text']
    ordering = ['order']

# Admin for Section
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['prefix', 'title']
    inlines = [QuestionInline]

# Admin for Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name']

# Admin for Subject
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']

# Admin for Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_subject', 'get_course', 'semester', 'academic_year']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Teacher Name'

    def get_subject(self, obj):
        return obj.subject.name if obj.subject else '-'
    get_subject.short_description = 'Subject'

    def get_course(self, obj):
        return obj.course.name if obj.course else '-'
    get_course.short_description = 'Course'

# Inline to view EvaluationItems in TeacherEvaluation
class EvaluationItemInline(admin.TabularInline):
    model = EvaluationItem
    extra = 0
    readonly_fields = ['get_section', 'get_question_number', 'question', 'rating', 'get_course', 'get_subject']
    can_delete = False

    # Section prefix
    def get_section(self, obj):
        return obj.question.section.prefix
    get_section.short_description = 'Section'

    # Question order
    def get_question_number(self, obj):
        return obj.question.order
    get_question_number.short_description = 'Question #'

    # Course from the teacher of the evaluation
    def get_course(self, obj):
        return obj.evaluation.teacher.course.name if obj.evaluation.teacher.course else '-'
    get_course.short_description = 'Course'

    # Subject from the teacher of the evaluation
    def get_subject(self, obj):
        return obj.evaluation.teacher.subject.name if obj.evaluation.teacher.subject else '-'
    get_subject.short_description = 'Subject'

# Admin for TeacherEvaluation
@admin.register(TeacherEvaluation)
class TeacherEvaluationAdmin(admin.ModelAdmin):
    list_display = [
        'get_teacher_name', 'get_subject', 'get_course',
        'get_semester', 'get_academic_year', 'overall_rating', 'submitted_at'
    ]
    readonly_fields = ['submitted_at']
    inlines = [EvaluationItemInline]

    def get_teacher_name(self, obj):
        return f"{obj.teacher.first_name} {obj.teacher.last_name}"
    get_teacher_name.short_description = 'Teacher Name'

    def get_subject(self, obj):
        return obj.teacher.subject.name if obj.teacher.subject else '-'
    get_subject.short_description = 'Subject'

    def get_course(self, obj):
        return obj.teacher.course.name if obj.teacher.course else '-'
    get_course.short_description = 'Course'

    def get_semester(self, obj):
        return obj.teacher.semester
    get_semester.short_description = 'Semester'

    def get_academic_year(self, obj):
        return obj.teacher.academic_year
    get_academic_year.short_description = 'Academic Year'

# Admin for EvaluationItem (optional: separate list view)
@admin.register(EvaluationItem)
class EvaluationItemAdmin(admin.ModelAdmin):
    list_display = [
        'evaluation', 'get_section', 'get_question_number', 'question',
        'rating', 'get_course', 'get_subject'
    ]

    def get_section(self, obj):
        return obj.question.section.prefix
    get_section.short_description = 'Section'

    def get_question_number(self, obj):
        return obj.question.order
    get_question_number.short_description = 'Question #'

    def get_course(self, obj):
        return obj.evaluation.teacher.course.name if obj.evaluation.teacher.course else '-'
    get_course.short_description = 'Course'

    def get_subject(self, obj):
        return obj.evaluation.teacher.subject.name if obj.evaluation.teacher.subject else '-'
    get_subject.short_description = 'Subject'

# ---------- Student Admin ----------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id']
    search_fields = ['student_id']