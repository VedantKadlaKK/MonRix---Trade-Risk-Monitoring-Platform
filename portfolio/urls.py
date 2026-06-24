from django.urls import path
from .views import (
    home,
    create_portfolio,
    portfolio_detail,
    add_trade,
    register,
    portfolio_api,
    trade_api
)

urlpatterns = [
    path("", home, name="home"),
    path("create/", create_portfolio, name="create_portfolio"),
    path(
        "portfolio/<int:pk>/",
        portfolio_detail,
        name="portfolio_detail"
    ),

    path(
        "portfolio/<int:portfolio_id>/add-trade/",
        add_trade,
        name="add_trade"
    ),
    path(
        "register/",
        register,
        name="register"
    ),
    path(
        "api/portfolios/",
        portfolio_api,
        name="portfolio_api"
    ),
    path(
        "api/trades/",
        trade_api,
        name="trade_api"
    ),
]