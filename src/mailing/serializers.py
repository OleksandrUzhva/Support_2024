from rest_framework import serializers


class EmailMessage(serializers.Serializer):
    sender = serializers.EmailField()
    recepient = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    body = serializers.CharField()
