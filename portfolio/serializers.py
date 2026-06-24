from rest_framework import serializers
from .models import Portfolio, Trade


class PortfolioSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Portfolio

        fields = [
            "id",
            "name",
            "risk_limit",
            "created_at"
        ]


class TradeSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Trade

        fields = "__all__"
