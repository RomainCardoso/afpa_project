from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, HiddenForm
from bs4 import BeautifulSoup
import sys, time, os, requests
from selenium import webdriver
from django.contrib.auth.decorators import login_required
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from .models import Search, Favorite
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test



def add_favorite(request):
    if request.method == 'POST':
        form = HiddenForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            amazon_price = form.cleaned_data.get('amazon_price')
            ldlc_price = form.cleaned_data.get('ldlc_price')
            maxgaming_price = form.cleaned_data.get('maxgaming_price')
            amazon_url = form.cleaned_data.get('amazon_url')
            ldlc_url = form.cleaned_data.get('ldlc_url')
            maxgaming_url = form.cleaned_data.get('maxgaming_url')
            user = request.user
            added_favorite = Favorite(name=user, amazon_price=amazon_price, ldlc_price=ldlc_price, maxgaming_price=maxgaming_price, amazon_url=amazon_url, ldlc_url=ldlc_url, maxgaming_url=maxgaming_url, searched_user=user)
            added_favorite.save()
