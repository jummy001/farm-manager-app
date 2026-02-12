from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from .forms import CategoryForm
import json
import csv
from django.http import HttpResponse

# -----------------------------
# Dashboard
# -----------------------------
@login_required
def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    low_stock_products = Product.objects.filter(quantity__lte=5)

    categories = Category.objects.annotate(
        product_count=Count('product')
    )

    labels = [cat.name for cat in categories]
    data = [cat.product_count for cat in categories]

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'low_stock_products': low_stock_products,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    }

    return render(request, 'products/dashboard.html', context)

# -----------------------------
# Product Views
# -----------------------------

@login_required
def product_list(request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')

    products = Product.objects.all()

    if search_query:
        products = products.filter(name__icontains=search_query)

    if sort_by:
        products = products.order_by(sort_by)

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    return render(request, 'products/list.html', context)


@login_required
def product_add(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        description = request.POST.get('description')

        category = get_object_or_404(Category, id=category_id)

        Product.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            description=description
        )

        messages.success(request, f'Product "{name}" added successfully!')
        return redirect('product_list')

    return render(request, 'products/add.html', {'categories': categories})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, id=pk)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id)
        product.description = request.POST.get('description')
        product.save()

        messages.success(request, f'Product "{product.name}" updated successfully!')
        return redirect('product_list')

    return render(request, 'products/edit.html', {
        'product': product,
        'categories': categories
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, f'Product "{product.name}" deleted successfully!')
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {
        'product': product
    })


# -----------------------------
# Category Views
# -----------------------------

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {
        'categories': categories
    })


@login_required
def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'products/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'products/category_form.html', {
        'form': form,
        'title': 'Edit Category'
    })


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('category_list')

    return render(request, 'products/category_confirm_delete.html', {
        'category': category
    })




@login_required
def export_products_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Price', 'Quantity', 'Category'])

    products = Product.objects.all()

    for product in products:
        writer.writerow([
            product.name,
            product.price,
            product.quantity,
            product.category.name
        ])

    return response
