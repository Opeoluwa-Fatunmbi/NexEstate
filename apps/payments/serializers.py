from rest_framework import serializers
from apps.payments.models import Payment


class PaymentSerializer(serializers.Serializer):
    """
    Payment serializer
    """

    id = serializers.IntegerField(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_name = serializers.CharField(required=True)
    product_image = serializers.URLField(required=True)
    amount = serializers.IntegerField(required=True)
    status = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(required=True)
    session_id = serializers.CharField(read_only=True)
    reference = serializers.CharField(read_only=True)
    transaction_id = serializers.CharField(read_only=True)
    transaction_date = serializers.DateTimeField(read_only=True)
    transaction_status = serializers.CharField(read_only=True)

    def create(self, validated_data):
        """
        Create a payment
        """
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update a payment
        """
        instance.status = validated_data.get("status", instance.status)
        instance.session_id = validated_data.get("session_id", instance.session_id)
        instance.reference = validated_data.get("reference", instance.reference)
        instance.transaction_id = validated_data.get(
            "transaction_id", instance.transaction_id
        )
        instance.transaction_date = validated_data.get(
            "transaction_date", instance.transaction_date
        )
        instance.transaction_status = validated_data.get(
            "transaction_status", instance.transaction_status
        )
        instance.transaction_reference = validated_data.get(
            "transaction_reference", instance.transaction_reference
        )
        instance.save()
        return instance
