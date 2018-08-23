from rest_framework import serializers
from users.models import User, Job


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    user_job = serializers.SerializerMethodField()

    def get_user_job(self, obj):
        user_job_qs = Job.objects.filter(user=obj)
        if user_job_qs.exists():
            user_job_qs = user_job_qs.first()
            serializer = JobSerializer(user_job_qs)
        else:
            intial_data = dict(self.initial_data)
            serializer = JobSerializer(data={'company_name': intial_data['company_name'][0],
                                             'company_type': intial_data['company_type'][0],
                                             'designation': intial_data['designation'][0],
                                             'email': intial_data['email'][0],
                                             })
            if serializer.is_valid():
                Job.objects.create(user=obj)
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)
        return JobSerializer(serializer.data).data

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'user_job', 'password')
        extra_kwargs = {'password': {'write_only': True}}

from mutual import constant
class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        required=True, max_length=127, error_messages={"blank": "Company name is required",
                                                       "required": "Company name is required",
                                                       "max_length": "Company name should be of maximum 127 characters"
                                                       })
    company_type = serializers.CharField(max_length=127)
    designation = serializers.CharField(max_length=127)
    email = serializers.CharField(max_length=127)

    def create(self, validated_data):

        job_obj = Job.objects.get(user__email=validated_data['email'])
        for attr, value in validated_data.items():
            setattr(job_obj, attr, value)
        job_obj.save()
        return job_obj

    def update(self, instance, validated_data):

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        """
        Define fields for this serializer
        """
        model = Job
        fields = ('id', 'company_name', 'company_type', 'designation', 'email')
