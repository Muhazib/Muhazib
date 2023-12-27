from django.shortcuts import render , redirect , HttpResponseRedirect,get_object_or_404
from store.models.product import Products
from store.models.category import Category
from django.views import View
from store.models.carousel import CarouselImage

# Create your views here.
class Index(View):
    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)
def home(request):
    # Retrieve a queryset of FoodItem objects
    food_items = Category.objects.all()
    carousel_images = CarouselImage.objects.all()
    # Use a dictionary to keep track of added categories
    added_categories = {}

    # Create a list to store unique food items
    unique_food_items = []

    # Iterate through all food items
    for item in food_items:
        # Check if the category is already added
            # Add the category to the dictionary
        added_categories[item.name] = True

            # Add the item to the unique_food_items list
        unique_food_items.append(item)

    # Pass the queryset to the template context
    context = {'food_items': unique_food_items,'carousel_images': carousel_images}

    # Render the template with the context
    return render(request, 'home.html', context)
def food_detail(request, food_id):
    food = get_object_or_404(Category, pk=food_id)
    # other_foods = Category.objects.filter(category=food.category).exclude(pk=food_id)
    return render(request, 'food_detail.html', {'food': food})
