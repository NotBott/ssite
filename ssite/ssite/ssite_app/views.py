from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib import auth

# def index(request):
#     products = models.Product.objects.all()
#     categories = models.Category.objects.all()
#     context = {
#         'products': products,
#         'categories': categories,
#     }
#
#     return render(request, 'ssite_app/index.html', context)


from itertools import chain


def index(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()

    if request.user.is_authenticated:
        visited_categories = models.UserVisit.objects.filter(user=request.user).order_by('-visit_count')

        if visited_categories.exists():
            top_category = visited_categories.first().category
            top_category_products = products.filter(category=top_category)

            other_products = products.exclude(category=top_category)

            products = list(chain(top_category_products, other_products))

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'ssite_app/index.html', context)


def category(request, pk):
    categories = models.Category.objects.all()
    current_category = models.Category.objects.get(pk=pk)
    products = models.Product.objects.filter(category=current_category)
    context = {
        'categories': categories,
        'current_category': current_category,
        'products': products
    }
    return render(request, 'ssite_app/category.html', context)


def favourites(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products = models.Product.objects.all()

    favorites = models.Favorites.objects.filter(user=request.user)

    context = {
        'products': products,
        'favorites': favorites
    }
    return render(request, 'ssite_app/favourites.html', context)


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    products = models.Product.objects.all()
    baskets = models.Basket.objects.filter(user=request.user)

    total_sum = 0
    for i in baskets:
        total_sum += i.sum()

    context = {
        'products': products,
        'baskets': baskets,
        'total_sum': total_sum,
    }
    return render(request, 'ssite_app/profile.html', context)


def user_login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('/')
    else:
        form = forms.UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'ssite_app/login.html', context)


def user_registration(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = forms.UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'ssite_app/registration.html', context)


def user_logout(request):
    auth.logout(request)
    return redirect('/')


from django.db.models import F


def detail(request, pk):
    product = models.Product.objects.get(pk=pk)
    productimages = models.ProductImage.objects.filter(product=product)

    is_favorite = models.Favorites.objects.filter(product=product).exists()

    comments = models.Comment.objects.filter(product=product)

    if request.user.is_authenticated:
        visit, created = models.UserVisit.objects.get_or_create(
            user=request.user,
            category=product.category
        )
        visit.visit_count += 1
        visit.save()

    if request.method == 'POST':
        form = forms.CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product = product
            if form.recall > 5:
                form.recall = 5

            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        form = forms.CommentForm()

    for comment in comments:
        comment.stars = range(comment.recall)

    context = {
        'product': product,
        'productimages': productimages,
        'is_favorite': is_favorite,
        'comments': comments,
        'form': form,
    }

    return render(request, 'ssite_app/detail.html', context)


def basket_add(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = models.Product.objects.get(pk=pk)
    baskets = models.Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        models.Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def basket_quantity_p(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = models.Product.objects.get(pk=pk)
    baskets = models.Basket.objects.filter(user=request.user, product=product)

    basket = baskets.first()
    basket.quantity += 1
    basket.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def basket_quantity_m(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = models.Product.objects.get(pk=pk)
    baskets = models.Basket.objects.filter(user=request.user, product=product)

    basket = baskets.first()
    basket.quantity -= 1
    basket.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


def basket_remove(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    basket = models.Basket.objects.get(pk=pk)
    basket.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def Favorites_add(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    product = models.Product.objects.get(pk=pk)

    models.Favorites.objects.create(user=request.user, product=product)

    return redirect(request.META.get('HTTP_REFERER', '/'))


def Favorites_remove(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    product = models.Product.objects.get(pk=pk)
    favorites = models.Favorites.objects.get(user=request.user, product=product)
    favorites.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


def search(request):
    query = request.GET.get('q', '')  # Получение строки поиска
    products = []
    if query:
        products = models.Product.objects.filter(name__icontains=query)  # Поиск по подстроке
    context = {
        'products': products,  # Передаем правильное имя переменной
    }
    return render(request, 'ssite_app/search_results.html', context)
