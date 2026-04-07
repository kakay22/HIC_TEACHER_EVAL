from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path("validate-evaluation/", views.validate_evaluation, name="validate_evaluation"),
    path('thank-you/', views.thank_you, name="thank_you"),
    path('admin-login/', views.admin_login, name="admin_login"),
    path('admin-logout/', views.admin_logout, name="admin_logout"),
    path('dashboard-home/', views.dashboard_home, name="dashboard_home"),
    path('teachers/', views.teachers_list, name='teachers_list'),
    path('teachers/search/', views.teacher_search, name='teacher_search'),
    #api teacher json
    path('api/teachers/', views.teacher_list_json, name='teacher_list_json'),
    path('evaluations-list/', views.evaluations_list, name='evaluations_list'),
    path('evaluations/<int:evaluation_id>/', views.evaluation_detail, name='evaluation_detail'),

    path('sections/', views.sections_list, name='sections_list'),
    path('sections/add/', views.section_add, name='section_add'),
    path('sections/<int:pk>/edit/', views.section_edit, name='section_edit'),
    path('sections/<int:pk>/delete/', views.section_delete, name='section_delete'),

    path('sections/<int:section_id>/questions/add/', views.question_add, name='question_add'),
    path('questions/<int:question_id>/edit/', views.question_edit, name='question_edit'),
    path('questions/<int:pk>/delete/', views.question_delete, name='question_delete'),

    path('teachers/<int:pk>/detail/', views.teacher_detail, name='teacher_detail'),
    path('teachers/add/', views.teacher_add, name='teacher_add'),
    path('teachers/edit/<int:pk>/', views.teacher_edit, name='teacher_edit'),
    path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),

    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    path('subjects/', views.subjects_list, name='subjects_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/<int:pk>/edit/', views.subject_edit, name='subject_edit'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    # Forgot password for superuser
    path(
        'admin/forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='admins/admin_forgot_password.html',
            email_template_name='admins/admin_password_reset_email.html',
            subject_template_name='admins/admin_password_reset_subject.txt',
            success_url='/admin/forgot-password/done/'
        ),
        name='admin_forgot_password'
    ),
    path(
        'admin/forgot-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='admins/admin_forgot_password_done.html'
        ),
        name='admin_forgot_password_done'
    ),
    path(
        'admin/reset-password/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='admins/admin_reset_password_confirm.html',
            success_url='/admin/reset-password/complete/'
        ),
        name='admin_reset_password_confirm'
    ),
    path(
        'admin/reset-password/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='admins/admin_reset_password_complete.html'
        ),
        name='admin_reset_password_complete'
    ),

]
