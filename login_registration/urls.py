from django.urls import path
from .views import LoginView, LogoutView, CollegeRegistrationView, UserRegistrationView, \
                    UserCrudApi, UserProfileView, HomeView, delete_user
from django.contrib.auth.decorators import login_required


from django.contrib.auth.views import ( 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('login', LoginView.as_view(), name='login'),

    path('logout', login_required(LogoutView.as_view()), name='logout'),

    path('profile', login_required(UserProfileView.as_view()), name='profile'),

    path('college-registration', CollegeRegistrationView.as_view(), name='college-registration'),

    path('user-registration', login_required(UserRegistrationView.as_view()), name='user-registration'),

    path('user-registration/<int:pk>', delete_user),

    path('user-crud/<pk>', login_required(UserCrudApi.as_view()), name='user-crud'),

    path('password-reset/', PasswordResetView.as_view(template_name='password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

]
