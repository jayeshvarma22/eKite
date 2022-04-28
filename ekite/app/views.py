from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self, request):
  totalitem = 0
  if request.user.is_authenticated:
    	totalitem = len(Cart.objects.filter(user=request.user))
  Cellular = Product.objects.filter(category='C')
  Flat = Product.objects.filter(category='F')
  AirInflated = Product.objects.filter(category='AI')
  Bowed= Product.objects.filter(category='B')
  Macaw= Product.objects.filter(category='M')
  Manjha = Product.objects.filter(category='MA')
  return render(request, 'app/home.html', {'Cellular':Cellular, 'Flat':Flat, 'AirInflated':AirInflated, 'Bowed':Bowed, 'Macaw':Macaw,'Manjha':Manjha, 'totalitem':totalitem})


class ProductDetailView(View):
  def get(self, request, pk):
   product = Product.objects.get(pk=pk)
   item_already_in_cart = False
   if request.user.is_authenticated:
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
   return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
 user = request.user
 product_id= request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
   user = request.user
   cart = Cart.objects.filter(user=user)
   print(cart)
   amount = 0.0
   shipping_amount = 70.0
   total_amount = 0.0
   cart_product = [p for p in Cart.objects.all() if p.user == user]
   # print(cart_product)
   if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
   else:
      return render(request, 'app/emptycart.html')

def plus_cart(request):
   if request.method == 'GET':
     prod_id = request.GET['prod_id']
     c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
     c.quantity+=1
     c.save()
     amount = 0.0
     shipping_amount = 70.0
     total_amount = 0.0
     cart_product = [p for p in Cart.objects.all() if p.user == request.user]   
     for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
      

     data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount 
        }
     return JsonResponse(data)
    
    
def minus_cart(request):
   if request.method == 'GET':
     prod_id = request.GET['prod_id']
     c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
     c.quantity-=1
     c.save()
     amount = 0.0
     shipping_amount = 70.0
     total_amount = 0.0
     cart_product = [p for p in Cart.objects.all() if p.user == request.user]   
     for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
       

     data = {
            'quantity': c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount 
        }
     return JsonResponse(data)
    
def remove_cart(request):
   if request.method == 'GET':
     prod_id = request.GET['prod_id']
     c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
     c.delete()
     amount = 0.0
     shipping_amount = 70.0
     total_amount = 0.0
     cart_product = [p for p in Cart.objects.all() if p.user == request.user]   
     for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        

     data = {
            'amount':amount,
            'totalamount':amount + shipping_amount 
        }
     return JsonResponse(data)
    


def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})



def flat(request, data=None):
 if data == None:
    flatkites = Product.objects.filter(category='F')
 elif data == 'Fkites' or data == 'Skykites':
    flatkites = Product.objects.filter(category='F').filter(brand=data)
 elif data == 'below':
    flatkites = Product.objects.filter(category='F').filter(discounted_price__lt=50)
 elif data == 'above':
    flatkites = Product.objects.filter(category='F').filter(discounted_price__gt=50)
 return render(request, 'app/flat.html', {'flatkites':flatkites})

def macaw(request, data=None):
 if data == None:
    macawkites = Product.objects.filter(category='M')
 elif data == 'Mkites' or data == 'Skykites':
    macawkites = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
    macawkites = Product.objects.filter(category='M').filter(discounted_price__lt=50)
 elif data == 'above':
    macawkites = Product.objects.filter(category='M').filter(discounted_price__gt=50)
 return render(request, 'app/macaw.html', {'macawkites':macawkites})


def manjha(request, data=None):
 if data == None:
    manjhareels = Product.objects.filter(category='MA')
 elif data == 'Monokite' or data == 'Skykites' or data == 'Cobra':
    manjhareels = Product.objects.filter(category='MA').filter(brand=data)
 elif data == 'below':
    manjhareels = Product.objects.filter(category='MA').filter(discounted_price__lt=500)
 elif data == 'above':
    manjhareels = Product.objects.filter(category='MA').filter(discounted_price__gt=500)
 return render(request, 'app/manjha.html', {'manjhareels':manjhareels})

class CustomerRegistrationView(View):
  def get(self, request):
   form = CustomerRegistrationForm()
   return render(request, 'app/customerregistration.html', {'form':form})

  def post(self, request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
     messages.success(request, 'Congratulations!! Registered Successfully.')
     form.save()
    return render(request, 'app/customerregistration.html', {'form':form})
@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]  
  if cart_product: 
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
    totalamount = amount + shipping_amount

  return render(request, 'app/checkout.html', {'add': add, 'totalamount':totalamount, 'cart_items':cart_items})

@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
