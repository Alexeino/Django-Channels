import threading
from .models import *
import time
from faker import Faker
import random
from channels.layers import get_channel_layer


fake = Faker()
class CreateStudentThread(threading.Thread):
    
    def __init__(self , total):
        self.total = total
        threading.Thread.__init__(self)
    def run(self):
        try:
            print("Thread execution started...")
            channel_layer = get_channel_layer()
            current_total = 0
            for i in range(self.total):
                current_total += 1
                obj = Students.objects.create(
                    name = fake.name(),
                    email = fake.email(),
                    address = fake.email(),
                    age = random.randint(10,50)
                )

                channel_layer = get_channel_layer()
                data = {
                    'name': obj.name,'email':obj.email,'address':obj.address,'age':str(obj.age),
                    'current_total':current_total, 'total':self.total
                }
                async_to_sync(channel_layer.group_send)(
                    'new_consumer_group',{
                        'type':'send_notification',
                        'value': json.dumps(data)
                        }
                    )
        except Exception as e:
            print(e)