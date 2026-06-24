from django.shortcuts import render, redirect, get_object_or_404
from .models import Portfolio, Trade, MarketPrice
from .forms import PortfolioForm, TradeForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    PortfolioSerializer,
    TradeSerializer
)


def calculate_positions(trades):

    positions = {}

    for trade in trades:

        if trade.symbol not in positions:
            positions[trade.symbol] = 0

        if trade.trade_type == "BUY":
            positions[trade.symbol] += trade.quantity
        else:
            positions[trade.symbol] -= trade.quantity

    return positions


def calculate_exposure(trades):

    exposure = 0

    for trade in trades:

        value = trade.quantity * trade.price

        if trade.trade_type == "BUY":
            exposure += value
        else:
            exposure -= value

    return exposure


@login_required
def home(request):

    portfolios = Portfolio.objects.filter(
        owner=request.user
    )

    portfolio_count = portfolios.count()

    trade_count = Trade.objects.filter(
        portfolio__owner=request.user
    ).count()

    context = {
        "portfolios": portfolios,
        "portfolio_count": portfolio_count,
        "trade_count": trade_count
    }

    return render(
        request,
        "portfolio/portfolio_list.html",
        context
    )

@login_required
def create_portfolio(request):

    if request.method == "POST":

        form = PortfolioForm(request.POST)

        if form.is_valid():

            portfolio = form.save(
                commit=False
            )

            portfolio.owner = request.user

            portfolio.save()

            return redirect("home")

    else:

        form = PortfolioForm()

    return render(
        request,
        "portfolio/create_portfolio.html",
        {"form": form}
    )

@login_required
def portfolio_detail(request, pk):

    portfolio = get_object_or_404(
        Portfolio,
        pk=pk,
        owner=request.user
    )

    trades = portfolio.trades.all()

    symbol = request.GET.get("symbol")

    if symbol:

        trades = trades.filter(
            symbol__icontains=symbol
        )

    trade_type = request.GET.get(
        "trade_type"
    )

    if trade_type:

        trades = trades.filter(
            trade_type=trade_type
        )

    trade_count = trades.count()

    positions = calculate_position_analytics(
        trades
    )

    for symbol, data in positions.items():

        try:

            market = MarketPrice.objects.get(
                symbol=symbol
            )

            current_price = float(
                market.current_price
            )

        except MarketPrice.DoesNotExist:

            current_price = 0

        data["market_price"] = current_price

        data["unrealized_pnl"] = (
            current_price
            - data["avg_price"]
        ) * data["quantity"]

    total_exposure = calculate_exposure(
        trades
    )

    risk_breached = (
        total_exposure >
        float(portfolio.risk_limit)
    )

    context = {
        "portfolio": portfolio,
        "trades": trades,
        "positions": positions,
        "total_exposure": total_exposure,
        "risk_breached": risk_breached,
        "trade_count": trade_count
    }

    return render(
        request,
        "portfolio/portfolio_detail.html",
        context
    )

@login_required
def add_trade(request, portfolio_id):

    portfolio = get_object_or_404(
        Portfolio,
        pk=portfolio_id,
        owner=request.user
    )

    if request.method == "POST":

        form = TradeForm(request.POST)

        if form.is_valid():

            trade = form.save(
                commit=False
            )

            trade.portfolio = portfolio

            trade.save()

            return redirect(
                "portfolio_detail",
                pk=portfolio.id
            )

    else:

        form = TradeForm()

    return render(
        request,
        "portfolio/add_trade.html",
        {
            "portfolio": portfolio,
            "form": form
        }
    )

def calculate_position_analytics(trades):

    positions = {}

    for trade in trades:

        symbol = trade.symbol

        if symbol not in positions:

            positions[symbol] = {
                "quantity": 0,
                "buy_value": 0
            }

        if trade.trade_type == "BUY":

            positions[symbol]["quantity"] += trade.quantity

            positions[symbol]["buy_value"] += (
                trade.quantity * float(trade.price)
            )

        else:

            positions[symbol]["quantity"] -= trade.quantity

    for symbol, data in positions.items():

        qty = data["quantity"]

        if qty > 0:

            data["avg_price"] = (
                data["buy_value"] / qty
            )

        else:

            data["avg_price"] = 0

    return positions


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )


@api_view(["GET"])
def portfolio_api(request):

    portfolios = Portfolio.objects.filter(
        owner=request.user
    )

    serializer = PortfolioSerializer(
        portfolios,
        many=True
    )

    return Response(
        serializer.data
    )


@api_view(["GET"])
def trade_api(request):

    trades = Trade.objects.filter(
        portfolio__owner=request.user
    )

    serializer = TradeSerializer(
        trades,
        many=True
    )

    return Response(
        serializer.data
    )