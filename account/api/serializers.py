from rest_framework import serializers
from rest_framework.serializers import ValidationError
from ..models import User,MyProfile,Ticket,Message


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=[
            'id',
            'phone'
        ]
        extra_kwargs={
            'phone':{"required":True,"write_only":True}
        }
    
    def validate_phone(self,value:str):

        if not 10<=len(value)<=11:
            raise ValidationError("phone length error")
        if not value.isdigit():
            raise ValidationError("phone is not valid")
        
    
    def create(self, validated_data:dict):
        

        return super().create(validated_data)



class UserInShow(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=[
            'id',
            ''
        ]


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=MyProfile
        fields=[
            'id',
            'first_name',
            'last_name',
            'user','image',
            'created',
            'email',
        ]
        extra_kwargs={
            'id':{"read_only":True},
            'user':{"read_only":True},
            'created':{"read_only":True},
            'first_name':{"required":True},
            'last_name':{"required":True},
            'image':{"required":False},
            'email':{"required":True},
        }
    


    def update(self, instance:MyProfile, validated_data:dict):
        instance.first_name=validated_data.get("first_name")
        instance.last_name=validated_data.get("last_name")
        instance.image=validated_data.get("image")
        instance.email=validated_data.get("email")
        instance.save()
        return instance
    



class TicketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Ticket
        fields=[
            'id',
            'subject',
            'sender_user',
            'ticket_type',
            'department_type',
            'department_ticket_type',
            'emergency_type',
            'created'
        ]

        extra_kwargs={
            'id':{"read_only":True},
            'created':{"read_only":True},
            'sender_user':{"read_only":True},
            'subject':{"required":True},
            'ticket_type':{"required":True},
            'department_type':{"required":True},
            'department_ticket_type':{"required":True},
            'emergency_type':{"required":True},
        }
    
    def validate_subject(self,value):
        if len(value)<3:
            raise ValidationError("length error")
        return value

    def create(self, validated_data:dict):
        new_tk=Ticket(
            subject=validated_data.get("subject"),
            ticket_type=validated_data.get("ticket_type"),
            department_type=validated_data.get("department_type"),
            department_ticket_type=validated_data.get("department_ticket_type"),
            emergency_type=validated_data.get("emergency_type"),
        )
        new_tk.save()
        return new_tk





class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=Message
        fields=[
            'id',
            'sender_messager',
            'receiver_messager',
            'ticket',
            'message_file',
            'message',
            'created'

        ]
        
        extra_kwargs={
            'id':{"read_only":True},
            'created':{"read_only":True},
            'sender_messager':{"read_only":True},
            'ticket':{"read_only":True},
            'receiver_messager':{"read_only":True},
            'message_file':{"allow_null":True},
            'message':{"allow_null":True},

        }

    
    def create(self, validated_data:dict):
        m=Message(
            message=validated_data.get("message"),
            message_file=validated_data.get("message_file"),
            receiver_messager="admin"
        )
        m.save()
        return m


    def validate(self, attrs:dict):
        
        if not attrs.get("message") and not attrs.get('message_file'):
            raise ValidationError("message or file is required")
        return attrs