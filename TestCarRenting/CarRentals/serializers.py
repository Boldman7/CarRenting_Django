from rest_framework import serializers
from .models import Tech
from .models import User
from .models import ParseUser

class TechSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tech
        fields = '__all__'

class SignUpSerializer(serializers.Serializer):
    mobile = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

class SignVerifySerializer(serializers.Serializer):
    mobile = serializers.CharField(required=False)
    code = serializers.IntegerField(required=False)

class RequestVerifySerializer(serializers.Serializer):
    confirmation_hash = serializers.CharField(required=False)
    code = serializers.IntegerField(required=False)

class UserSerializer(serializers.Serializer):

    id = serializers.CharField(max_length=200)
    mobile = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=200)
    namespace = serializers.CharField(max_length=200)
    confirmation_hash = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
    href = serializers.CharField(max_length=200)
    target_id = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=200)
    updated = serializers.DateTimeField()

    access_token = serializers.CharField(max_length=200)
    client_id = serializers.CharField(max_length=200)
    code = serializers.CharField(max_length=200)
    endpoints_http = serializers.CharField(max_length=200)
    endpoints_mqtt = serializers.CharField(max_length=200)
    endpoints_uploader = serializers.CharField(max_length=200)
    expires = serializers.CharField(max_length=200)
    grant_type = serializers.CharField(max_length=200)
    owner_id = serializers.CharField(max_length=200)
    refresh_token = serializers.CharField(max_length=200)
    scope_1 = serializers.CharField(max_length=200)
    scope_2 = serializers.CharField(max_length=200)

    # def validate(self, validated_data):
    #     data = self.context['request'];
    #     validated_data['user_id'] = data.id
    #     validated_data['name'] = data.name
    #     validated_data['namespace'] = data.namespace
    #     validated_data['mobile'] = data.mobile
    #     validated_data['confirmation_hash'] = data.confirmation_hash
    #     validated_data['created_at'] = data.created
    #     validated_data['href'] = data.href
    #     validated_data['target_id'] = data.target_id
    #     validated_data['type'] = data.type
    #     validated_data['updated_at'] = data.updated
    #
    #     return validated_data

    # This will handle rename
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('id', instance.user_id)
        instance.name = validated_data.get("name", instance.name)
        instance.mobile = validated_data.get("mobile", instance.mobile)
        instance.namespace = validated_data.get("namespace", instance.namespace)
        instance.confirmation_hash = validated_data.get("confirmation_hash", instance.confirmation_hash)
        instance.target_id = validated_data.get("target_id", instance.target_id)
        instance.href = validated_data.get("href", instance.href)
        instance.type = validated_data.get("type", instance.type)
        instance.created_at = validated_data.get("created", instance.created_at)
        instance.updated_at = validated_data.get("updated", instance.updated_at)
        instance.save()
        return instance
    #
    # # this will handle POST - or layer upload
    def create(self, validated_data):

        user = User.objects.create(
            user_id = validated_data.get("id"),
            name = validated_data.get("name"),
            mobile = validated_data.get("mobile"),
            namespace = validated_data.get("namespace"),
            confirmation_hash = validated_data.get("confirmation_hash"),
            target_id = validated_data.get("target_id"),
            href = validated_data.get("href"),
            type = validated_data.get("type"),
            created_at = validated_data.get("created"),
            updated_at = validated_data.get("updated"))

class RequestVerifySerializer(serializers.Serializer):
    confirmation_hash = serializers.CharField(required=False)
    code = serializers.IntegerField(required=False)