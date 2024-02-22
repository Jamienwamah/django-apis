"""
Django settings for RentSpace project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
from decouple import AutoConfig

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
config = AutoConfig()


# Quick-start development settings
SECRETS_KEY = config('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rent.apps.RentConfig',
    'admin_control.apps.AdminControlConfig',
    'admin_history.apps.AdminHistoryConfig',
    'announcement.apps.AnnouncementConfig',
    'maintenance.apps.MaintenanceConfig',
    'pverification.apps.PVerificationConfig',
    'notification.apps.NotificationConfig',
    'bverification.apps.BverificationConfig',
    'loancreation.apps.LoancreationConfig',
    'chat.apps.ChatConfig',
    'loandebit.apps.LoandebitConfig',
    'loaninfo.apps.LoaninfoConfig',
    #'dva.apps.DvaConfig',
    'activities.apps.ActivitiesConfig',
    'rest_framework_simplejwt.token_blacklist',
    'cardverification.apps.CardverificationConfig',
    'listofsupportedbanks.apps.ListofsupportedbanksConfig',
    'adebitting.apps.AdebittingConfig',
    #'login.apps.LoginConfig',
    'landlord.apps.LandlordConfig',
    'otp.apps.OtpConfig',
    'accountdetails.apps.AccountdetailsConfig',
    #'dva_history.apps.DvaHistoryConfig',
    #'notifications.apps.NotificationsConfig',
    'bdebit.apps.BDebitConfig',
    'wallet.apps.WalletConfig',
    'reset.apps.ResetConfig',
    'forpass.apps.ForpassConfig',
    'kyc.apps.KycConfig',
    # 'bvn.apps.BvnConfig',
    # 'kyc_details.apps.Kyc_detailsConfig',
    # 'space_rent.apps.Space_rentConfig',
    'space_rent_creation.apps.SpaceRentCreationConfig',
    #'useractivities.apps.UserActivitiesConfig',
    'account.apps.AccountConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
]

RSIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
}
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RentSpace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'RentSpace.wsgi.application'

#Cors
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('RENTSPACE_DB'),
        'USER': config('RENTSPACE_USER'),
        'PASSWORD': config('RENTSPACE_PASS'),
        'HOST': config('RENTSPACE_HOST'),
        'PORT': config('RENTSPACE_PORT'),
    }
}


DATABASES = {
    "default": dj_database_url.parse("postgres://rentspaceuser:tysEWCeOw2o2DhBvUtaynKTNf1olsowg@dpg-cn5j4men7f5s738i8qag-a.oregon-postgres.render.com/rentspace_7xqu")
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Define the URL prefix to serve static files
STATIC_URL = '/static/'

# Define the directory where static files will be collected
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#Static file storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#AUTH_USER_MODEL = 'rent.CustomAppUser',
#AUTH_USER_MODEL = 'account.AccountUser',
#AUTH_USER_MODEL = 'bdebit.BvnDebitUser',
#AUTH_USER_MODEL = 'login.LoginUser',
#AUTH_USER_MODEL = 'useractivities.UserActivity'
#AUTH_USER_MODEL = 'everification.EmailVerification'


"""
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.MiddlewareEncryption',
    'admin_control.middleware.MiddlewareEncryption',
    'admin_history.middleware.MiddlewareEncryption',
    'announcement.middleware.MiddlewareEncryption',
    'bdebit.middleware.MiddlewareEncryption',
    'bverification.middleware.MiddlewareEncryption',
    'chat.middleware.MiddlewareEncryption',
    'everification.middleware.MiddlewareEncryption',
    'forpass.middleware.MiddlewareEncryption',
    'login.middleware.MiddlewareEncryption',
    'maintenance.middleware.MiddlewareEncryption',
    'notification.middleware.MiddlewareEncryption',
    'otp.middleware.MiddlewareEncryption',
    'pverification.middleware.MiddlewareEncryption',
    #'rent.middleware.MiddlewareEncryption',
    #'rent_history.middleware.MiddlewareEncryption',
    #'reset.middleware.MiddlewareEncryption',
    #'space_loan.middleware.MiddlewareEncryption',
    #'space_rent.middleware.MiddlewareEncryption',
    #'account.middleware.MiddlewareEncryption',
    #'account.middleware.MiddlewareEncryption',# Add your custom middleware here
]
"""

#Mail Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True 


#Watu key
CLIENT_KEY = config('client_key')
SECRET_KEY = config('server_key')
ENCRYYPTION_KEY = config('encryption_key')
IV_KEY = config('aes_iv_key')
"""
#Implemeting simple-jwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LIST_LOGIN': False,
    
    #'ALGORITHM': HS256,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'LEEWAY': 0,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt_authentication.default_user_authentication_rule',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
                                       
}

AUTHENTICATION_BACKENDS = [
    'rent.backends.CustomUserAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',  # This is the default backend
]
"""
