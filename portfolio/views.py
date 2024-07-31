# portfolio/views.py
from django.shortcuts import render
from .models import Portfolio

def portfolio_list(request):
    if request.user.is_authenticated:
        portfolios = Portfolio.objects.filter(user=request.user)
    else:
        portfolios = []
    return render(request, 'portfolio/portfolio_list.html', {'portfolios': portfolios})
