from rest_framework import serializers
from users.models import User, Job
from mutual import constant


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    user_job = serializers.SerializerMethodField()

    def get_user_job(self, obj):
        user_job_qs = Job.objects.filter(user=obj)
        if user_job_qs.exists():
            user_job_qs = user_job_qs.first()
            serializer = JobSerializer(user_job_qs)
        else:
            # while using post man i need to use .dict()
            # intial_data = self.initial_data.dict()
            intial_data = self.initial_data
            serializer = JobSerializer(data={'company_name': intial_data.get('company_name', None),
                                             'company_type': intial_data.get('company_type', None),
                                             'designation': intial_data.get('designation', None),
                                             'resume': intial_data.get('resume', None)
                                             },
                                       context={'user': obj})
            if serializer.is_valid():
                serializer.save()
                # Updating instance for the user for its job object
                # serializer.instance.user = obj
                # serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)
        return serializer.data

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'user_job', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        required=True, max_length=127, error_messages=constant.COMPANY_NAME_ERROR_MSG)
    company_type = serializers.ChoiceField(choices=constant.COMPANY_TYPE,
                                           error_messages=constant.COMPANY_TYPE_ERROR_MSG)
    designation = serializers.CharField(max_length=127, error_messages=constant.DESIGNATION_ERROR_MSG)

    def create(self, validated_data):
        job_obj = Job.objects.create(user=self.context.get('user'), **validated_data)
        return job_obj

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, obj):
        """
        :param obj: job instance
        :return: response to be modified here before returning as response
        """
        attr = super(JobSerializer, self).to_representation(obj)
        attr.__setitem__("user_id", obj.user.id)
        return attr

    class Meta:
        """
        Define fields for this serializer
        """
        model = Job
        fields = ('id', 'company_name', 'company_type', 'designation', 'resume')


from django.db.models.signals import post_save
from .signals import create_user_profile, create_user_job

post_save.connect(create_user_profile, sender=User)
post_save.connect(create_user_job, sender=Job)
