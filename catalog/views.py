from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse, redirect
from django.template import loader
from .models import Category, Subcategory, Product
from .forms import CategoryForm, SubcategoryForm, ProductForm, UploadProductImage

def index(request):
    try:
        product_list = Product.objects.all()
    except Product.DoesNotExist:
        raise Http404("No Products")
    template = loader.get_template('index.html')
    context = {
        'product_list': product_list,
    }
    return HttpResponse(template.render(context, request))


def departments(request):
    try:
        department_list = Category.objects.all()
    except Category.DoesNotExist:
        raise Http404("No Departments")
    template = loader.get_template('departments.html')
    context = {
        'department_list': department_list,
    }
    return HttpResponse(template.render(context, request))


def category(request,category_id):
    try:
        category_list = Subcategory.objects.filter(category=category_id)
    except Subcategory.DoesNotExist:
        raise Http404("No Categories")
    template = loader.get_template('category.html')
    context = {
        'category_list': category_list,
    }
    return HttpResponse(template.render(context, request))


def subcategory(request,subcategory_id):
    try:
        dict = Subcategory.objects.filter(id=subcategory_id).values('category')
        c_id = dict[0]
        subcategory_list = Product.objects.filter(subcategory=subcategory_id)
    except Product.DoesNotExist:
        raise Http404("No Products")
    template = loader.get_template('subcategory.html')
    context = {
        'subcategory_list': subcategory_list,
        'c_id': c_id['category']
    }
    return HttpResponse(template.render(context, request))


def product(request, product_id):
    try:
        product_details = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    template = loader.get_template('product.html')
    context = {
        'product_details': product_details,
    }
    return HttpResponse(template.render(context, request))


def add_category(request):
    title = 'Add New Category'
    form_class = CategoryForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments')
    return render(request, 'add_new.html', {'form_class': form_class, 'title':title})


def add_subcategory(request):
    title = 'Add New SubCategory'
    form_class = SubcategoryForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'add_new.html', {'form_class': form_class, 'title': title})


def add_product(request):
    title = 'Add New Product'
    if request.method == 'POST':
        form = UploadProductImage(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    form_class = UploadProductImage
    return render(request, 'add_new.html', {'form_class': form_class, 'title': title})

