from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError  # Import IntegrityError
from django.core.validators import MinLengthValidator
from datetime import datetime
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    first_name = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Please input your first name.',
    })
    last_name = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Please input your last name.',
    })
    username = serializers.CharField(write_only=True, required=True, min_length=7, error_messages={
        'required': 'Input username.',
        'min_length': 'Username must be at least 7 characters long.',
    })
    email = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Email is needed.',
    })
    phone_number = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Input phone number.',
    })
    date_of_birth = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Enter your date of birth.',
    })
    password = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Input a password',
    })
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, required=True, error_messages={
        'required': 'Enter your gender.',
    })
    residential_address = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'Enter residential address.',
    })

    class Meta:
        model = User
        fields = '__all__'
        
    def validate_first_name(self, value):
        # Custom first_name validation logic
        if value.strip() == '':
            raise serializers.ValidationError('Please input your first name.')
        return value

    def validate_last_name(self, value):
        # Custom last_name validation logic
        if value.strip() == '':
            raise serializers.ValidationError('Please input your last name.')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_email(self, value):
        # Custom email validation logic
        if value.strip() == '':
            raise serializers.ValidationError('Email is needed.')
        return value
    
    def validate_phone_number(self, value):
        # Ensure the phone number is in the format +234XXXXXXXXXX
        if not value.startswith('+234'):
            raise serializers.ValidationError('Phone number must start with +234.')
        if len(value) != 14:  # Length should be 14 characters including the country code
            raise serializers.ValidationError('Invalid phone number format.')
        return value
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number must be unique.")
        return value
    
    def validate_date_of_birth(self, value):
        try:
            # Attempt to parse the date with the expected format
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            # Raise a ValidationError with the custom message if the format is invalid
            raise serializers.ValidationError('Date of birth must be in YYYY-MM-DD format.')
        return value
    
    def validate_password(self, value):
        # Custom password validation logic
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")

        # Check for at least one special character from the specified set
        if not re.search(r'[#!%&$@*]', value):
            raise serializers.ValidationError("Password must contain at least one special character from (#!%&$@*).")

        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def validate_gender(self, value):
        # Custom gender validation logic
        if value.strip() == '':
            raise serializers.ValidationError('Enter your gender.')
        return value
    
    def validate_residential_address(self, value):
        # Custom residential_address validation logic
        if value.strip() == '':
            raise serializers.ValidationError('Enter residential address.')
        return value
    

    """def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            date_of_birth=validated_data.get('date_of_birth'),
            password=validated_data.get('password'),
            gender=validated_data.get('gender'),
            residential_address=validated_data.get('residential_address'),
        )
        return user
    """
    
    def create(self, validated_data):
        try:
            user = User.objects.create(**validated_data)
        except IntegrityError as e:
            if 'phone_number' in e.args[0]:  # Handle phone number integrity error
                raise serializers.ValidationError({"error":{"phone_number":["Phone number must be unique."]}})
            elif 'username' in e.args[0]:  # Handle username integrity error
                raise serializers.ValidationError({"error": {"username": ["Username already exists."]}})
            elif 'email' in e.args[0]:  # Handle email integrity error
                raise serializers.ValidationError({"error": {"email": ["Email already exists."]}})
            else:
                # Handle other integrity errors if needed
                raise serializers.ValidationError({"error":["An error occurred while creating the user."]})
        else:
            # If no exception is raised, return a success message with 200 OK status
            return {"Registration was successful"}

