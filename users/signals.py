from mutual.utils import write_log
def create_user_profile(sender, instance, created, **kwargs):
    action = "User created"
    write_log(instance, action)
    print('user created with id '+str(instance.id)+' and email '+instance.email)


def create_user_job(sender, instance, created, **kwargs):
    action = "Job created"
    write_log(instance, action)
    print('user job created with id '+str(instance.id))
