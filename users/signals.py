def create_user_profile(sender, instance, created, **kwargs):
    print('user created with id '+str(instance.id)+' and email '+instance.email)


def create_user_job(sender, instance, created, **kwargs):
    print('user job created with id '+str(instance.id))
