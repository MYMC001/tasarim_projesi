from django.shortcuts import render ,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login ,logout ,authenticate
from django.contrib.auth.decorators import login_required ,permission_required

from django.views.generic.base import RedirectView
from Jib.models import CustomUser
@login_required
def Home(request):

    if request.user.is_delivier:  
        return redirect('deliver')
    if hasattr(request.user, 'restaurant') and request.user.restaurant:
                return redirect(reverse('res_home', args=[request.user.restaurant.id]))
    restaurants=Restaurant.objects.all()
    return render (request ,'index.html' ,{'restaurants':restaurants })
   


def  create_account(request):
   if request.method=="POST":
       yeni_username=request.POST.get('username')
       email=request.POST.get('email')
       password=request.POST.get('password')
       confirm_password=request.POST.get('confirm_password')

       if CustomUser.objects.filter(username=yeni_username).exists() :
           messages.error(request ,'Bu isim zaten mevcut')
           return redirect('login')
       if(confirm_password != password):
           messages.error(request ,'şifre aynı değil')
           return redirect('login')
       else:
        CustomUser.objects.create_user(username=yeni_username ,email=email ,password=password)
        messages.success(request ,'account created !!')
        return redirect('login')
   else:
        return redirect('login')    
   

from django.conf import settings



def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('login')






@login_required
def favorite(request):
   return render( request   ,'user_is_things/favorite.html')



def reset_info(request):
    if request.method=='POST':
        yeni_username=request.POST.get('username')
        user_id=request.POST.get('user_id')
        user=CustomUser.objects.get(pk=user_id)
        user.username=yeni_username
        user.save()
        return redirect('profile')    
    return redirect('profile')    


def reset_password(request):
    if request.method=='POST':
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        user_id=request.POST.get('user_id')
        user=CustomUser.objects.get(pk=user_id)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            log_out(request)
            return redirect('login')
        else:
            return redirect('profile')    
    return redirect('profile')    


@login_required
# @permission_required('Jib.have_restaurant')   
def res_home(request, res_id):
   
    restaurant = Restaurant.objects.get(pk=res_id)    
    last_order_for_restaurant = restaurant.orders.filter(is_confirmed=False).last()
    if last_order_for_restaurant:
        order = request.user.orders.filter(is_confirmed=False).last()
        left=restaurant.minimum-last_order_for_restaurant.total_price
        return render(request, 'restaurant_is_things/res_index.html', {'restaurant': restaurant, 'order': order ,'left':left})
    else:
        return render(request, 'restaurant_is_things/res_index.html', {'restaurant': restaurant})




     


from Jib.models import Restaurant
from Jib.models import Product
def add_product(request):
    if request.method=="POST":
       restaurant_id=request.POST.get('restaurant_id')
       name=request.POST.get('name')
       price=request.POST.get('price')
       discription=request.POST.get('discription')
       type=request.POST.get('type')    
       image = request.FILES.get('image')  # Use request.FILES
       restaurant= Restaurant.objects.get(pk=restaurant_id)
       if Product.objects.filter(name=name).exists():
           messages.error(request ,f'Bu ürün eklendi {name}')
           return redirect('res_home' ,)
       if  name:
           Product.objects.create(name=name ,price=price ,discription=discription ,type=type ,image=image ,restaurant=restaurant)
           return redirect(reverse('res_home', kwargs={'res_id': restaurant.id}))
       else:
           return redirect(reverse('res_home', kwargs={'res_id': restaurant.id}))
    else:
        return redirect(reverse('res_home', kwargs={'res_id': restaurant.id}))


from Jib.models import Order



from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

def add_item_toOrder(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        restaurant_id = request.POST.get("restaurant_id")

        product = get_object_or_404(Product, pk=product_id)
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

        order = request.user.orders.filter(restaurant=restaurant, is_confirmed=False).first()

        with transaction.atomic():
            if order:  
                item = order.items.filter(product=product).first()
                if item:  
                    item.quantity += 1
                    item.total_price += product.price
                    item.save()
                else: 
                    item = order.items.create(product=product, quantity=1, total_price=product.price)

                order.total_price += product.price
                order.save()

            else:  
                order = request.user.orders.create(restaurant=restaurant, user=request.user)
                restaurant.orders_quantity+=1
                restaurant.save()
                item = order.items.create(product=product, quantity=1, total_price=product.price)
                order.total_price = item.total_price
                order.save()
        return redirect(reverse('res_home', kwargs={'res_id': restaurant.id}))
    return redirect(reverse('res_home', kwargs={'res_id': restaurant_id}))


from Jib.models import OrderItem    

from django.urls import reverse

def descrement_item(request, item_id):
    item = OrderItem.objects.get(pk=item_id)
    res_id = item.order.restaurant.id
    if item.quantity == 0:
        return redirect(reverse('res_home', kwargs={'res_id': res_id}))
    item.quantity -= 1
    item.save()
    item.total_price-=item.product.price
    item.save()
    item.order.total_price -= item.product.price
    item.order.save()  
    return redirect(reverse('res_home', kwargs={'res_id': res_id}))
    
def increment_item(request ,item_id):
     item=OrderItem.objects.get(pk=item_id)
     item.quantity=item.quantity+1
     item.save()
     item.total_price+=item.product.price
     item.save()
     item.order.total_price += item.product.price
     item.order.save()  
     res_id=item.order.restaurant.id
     return redirect(reverse('res_home', kwargs={'res_id': res_id}))
        
def deleteAll_items(request ,item_id):
    item=OrderItem.objects.get(pk=item_id)
    res_id=item.order.restaurant.id
    item.order.delete()
    return redirect(reverse('res_home', kwargs={'res_id': res_id}))

    

def order_confirm(request ,order_id):
    order=Order.objects.get(pk=order_id) 
    return redirect(reverse('confirm' ,kwargs={'order_id':order.id}))

def confirm(request ,order_id):
    order=Order.objects.get(pk=order_id)
    r=order.restaurant
    toplam=r.teslimat_ucreti+order.total_price+order.tip_value
    hizmet_ucreti=(r.res_hizmet*toplam)/100
    toplam+=hizmet_ucreti
    return render(request ,'user_is_things/confirm.html' ,{'order':order ,'toplam':toplam ,'hizmet_ucreti':hizmet_ucreti})



def order_complet(request ,order_id):
    order=Order.objects.get(pk=order_id)
    order.is_confirmed=True
    order.save()
    payment=order.payment
    if payment.payment_type == 'Online' :
        payment.is_payed=True
        payment.save()
    r= order.restaurant
    r.new_orders+=1
    r.save()
    return redirect(reverse('complet' ,kwargs={'order_id':order.id}))



def complet(request ,order_id):
    order=Order.objects.get(pk=order_id)
    return render(request ,'user_is_things/complet.html' ,{'order':order})



def update_product(request ,product_id):
       product=Product.objects.get(pk=product_id)
       return render(request ,'restaurant_is_things/add_product.html',{'product':product} )

def delete_product(request ,product_id):
    product=Product.objects.get(pk=product_id)
    res_id=product.restaurant.id
    product.delete()
    return redirect(reverse('res_home' ,kwargs={'res_id':res_id}))

def confirm_productUpdate(request):
        
        if request.method=="POST":
            product_id=request.POST.get('product_id')
            name=request.POST.get('name')
            price=request.POST.get('price')
            discription=request.POST.get('discription')
            type=request.POST.get('type')

            product=Product.objects.get(pk=product_id)
            if product:
             product.price=price
             product.name=name
             product.discription=discription
             product.type=type
             product.save()

            return redirect(reverse('res_home' ,kwargs={'res_id':product.restaurant.id}))
                    
        return update_product(request ,product.id)




def Orders(request):
    new_orders=request.user.restaurant.orders.filter(is_on_way = False)
    status=False
    if new_orders :
        status =True

    
    return render(request ,'restaurant_is_things/neworders.html' ,{'orders':new_orders  ,'status':status})


def  Order_tooked(request ,order_id):
    order=Order.objects.get(pk=order_id)
    r=order.restaurant
    r.new_orders-=1
    r.save()
    order.is_accepted=True
    order.save()
    order.order_image="wait"
    order.save()
    order.order_stepDes="hazırlanıyor"
    order.save()
    return redirect(reverse('Orders'))


def  canceled(request ,order_id):
    order=Order.objects.get(pk=order_id)
    order.is_canceled=True
    order.save()
    r=order.restaurant
    r.new_orders-=1
    r.save()
    order.order_stepDes="Iptal edildi !"
    order.save()
    return redirect(reverse('Orders'))


from Jib.models import Favorite
def Res_favorite(resquest):
    if resquest.method == "POST":
        restaurant_id=resquest.POST.get('restaurant_id')
        user_id=resquest.POST.get('user_id')
        restaurant=Restaurant.objects.get(pk=restaurant_id)
        user=User.objects.get(pk=user_id)
        for favorite in Favorite.objects.all():
            if favorite.restaurant == restaurant and favorite.user == user and favorite.is_favorite == True :
                favorite.delete()
                return redirect('home')
        Favorite.objects.create(user=user ,restaurant=restaurant ,is_favorite=True)
        return redirect('home')
    
    return redirect('home')


def addressler(request):
    return render(request ,'user_is_things/addres.html' ,{})



from Jib.models import Address
def add_adress(request):
    if request.method == "POST":

        user_id=request.POST.get('user_id')
        il=request.POST.get('il')
        mahalle=request.POST.get('mahalle')
        bina=request.POST.get('bina')
        daire=request.POST.get('daire')
        kat=request.POST.get('kat')
        sokak=request.POST.get('sokak')
        telefon=request.POST.get('telefon')
        tamdres=request.POST.get('tamadres')
        user=User.objects.get(pk=user_id)
        if user :
            Address.objects.create(user=user ,city=il ,street=sokak ,neighborhood=mahalle ,building_name=bina ,apartment_n=daire ,floor_num=kat,phone=telefon ,full_adress=tamdres)
            return redirect(reverse('home'))
    return redirect(reverse('addressler'))    

from Jib.models import Payment

from django.core.exceptions import ObjectDoesNotExist

def payment(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        paymenttype = request.POST.get("paymenttype")
        
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return redirect('error_page')  
        try:
            if order.payment: 
                order.payment.payment_type = paymenttype
                order.payment.save()
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            Payment.objects.create(order=order, payment_type=paymenttype)
        
        return redirect(reverse('confirm', kwargs={'order_id': order.id}))    
    return redirect(reverse('confirm', kwargs={'order_id': order.id}))


def tip(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        tip = request.POST.get("tip")
        
        if tip:
            try:
                tip = int(tip)  
            except ValueError:
                return redirect(reverse('confirm', kwargs={'order_id': order_id}))
        else:
            return redirect(reverse('confirm', kwargs={'order_id': order_id}))  
        order = Order.objects.get(pk=order_id)

        if order:
            if order.is_tip == False:
                order.is_tip = True
                order.save()
                order.tip_value = tip
                order.save()
                order.Toplam+=order.restaurant.teslimat_ucreti
                order.save()
                order.Toplam+=order.tip_value
                order.save()
                return redirect(reverse('confirm', kwargs={'order_id': order.id}))
            else:
                order.tip_value=0
                order.save()
                order.tip_value = tip
                order.save()
                order.Toplam+=order.restaurant.teslimat_ucreti
                order.save()
                order.Toplam+=order.tip_value
                order.save()
               
                return redirect(reverse('confirm', kwargs={'order_id': order.id}))
        
    return redirect(reverse('confirm', kwargs={'order_id': order.id}))

        

def tip_later(request):
    if request.method == "POST":
        order_id=request.POST.get("order_id")
        order=Order.objects.get(pk=order_id)
        order.tip_value=0
        order.save()
        order.is_tip=False
        order.save()
        return redirect(reverse('confirm', kwargs={'order_id': order.id})) 
    return redirect(reverse('confirm', kwargs={'order_id': order.id})) 
     




def forout(request ,order_id):

    
    order=Order.objects.get(pk=order_id)

    if order.is_accepted == False :
         messages.info(request ,'Sipariş kabul edilmedi yada yola çıkmadı müşteriye bilgi gönder')
         return redirect(reverse('Orders'))
    
   
    
    order.is_on_way=True
    order.save()
    order.order_image="deliveryLogo"
    order.save()
    order.order_stepDes="yola çıktı"
    order.save()
    return redirect(reverse('Orders'))


from django.contrib import messages

def delivred(request ,order_id):
    order=Order.objects.get(pk=order_id)
    if order.is_accepted == False or order.is_on_way == False :
         messages.info(request ,'Sipariş kabul edilmedi yada yola çıkmadı müşteriye bilgi gönder')
         return redirect(reverse('Orders'))
    order.is_delivered=True
    order.save()
    order.order_image="delivred"
    order.save()
    order.order_stepDes="teslim edildi"
    order.save()
    r=order.restaurant
    r.new_orders-=1
    r.save()
 
    return redirect(reverse('Orders'))

def siparislerim( request):
    orders=request.user.orders.all().order_by('is_delivered')
    return render(request ,'user_is_things/siparislerim.html' ,{'orders':orders})


from Jib.models import User_Message
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def send_message(request):
    if request.method == "POST":
        content = request.POST.get("content")
        restaurant_id = request.POST.get("restaurant_id")
        restaurant=Restaurant.objects.get(pk=restaurant_id)
        sender = request.user
        User_Message.objects.create(sender=sender, receiver=restaurant.user, restaurant=restaurant, value=content )
        return redirect(reverse('user_message', kwargs={'res_id': restaurant.id}))
    

def res_send_message(request):
     if request.method == "POST":
        user_id = request.POST.get("user_id")
        restaurant=request.POST.get('res_id')
        restaurant=Restaurant.objects.get(pk=restaurant)
        content = request.POST.get("content")
        sender = request.user
        receiver=CustomUser.objects.get(pk=user_id)
        User_Message.objects.create(sender=sender, receiver=receiver, restaurant=restaurant, value=content )
        return redirect(reverse('message_container' ,kwargs={'user_id':receiver.id}))
    
 


def messager(request):
    AllOfmessages = User_Message.objects.all()
    return render(
        request,
        'restaurant_is_things/message.html',
        { 'messages': AllOfmessages}
    )

def message_container(request ,user_id):
    user=CustomUser.objects.get(pk=user_id)
    u_messages = User_Message.objects.all()
    AllOfmessages = User_Message.objects.all()
    return render(request ,'restaurant_is_things/m_container.html' ,{'sender':user ,'u_messages': u_messages , 'messages': AllOfmessages})

def user_message(request ,res_id):
    restaurant=Restaurant.objects.get(pk=res_id)
    u_message=User_Message.objects.all()
    return render (request ,'user_is_things/user_message.html' ,{'restaurant':restaurant ,'messages':u_message})


def deliver(request):
    orders=Order.objects.all()
    return render(request ,'user_is_things/deliver.html' ,{'orders':orders})


from Jib.models import Order_Deliver
def take_order(request):

    if  request.method == 'POST':
        order_id=request.POST.get('order_id')
        user_id=request.POST.get('user_id')
        order=Order.objects.get(pk=order_id)
        user=CustomUser.objects.get(pk=user_id)

        if user.deliver_num ==2 :

            messages.info(request ,f'You have {request.user.deliver_num} active orders')
            return redirect('deliver')
        else:
            order.is_accepted_fd=True
        order.save()
        user.deliver_num+=1
        user.save()
        Order_Deliver.objects.create(user=user, order=order)
        return redirect('deliver')
    return redirect('deliver')

    

def deliveier_status(request):

    if request.method == "POST":

        user_id=request.POST.get('user_id')
        user=CustomUser.objects.get(username=user_id)

        if user.is_active_f_order :

            user.is_active_f_order = False
            user.save()

            return redirect("deliver")
        else:
              user.is_active_f_order = True
              user.save()
              return redirect("deliver")
    return redirect("deliver")





def active_order(request):

    return render(request ,'user_is_things/active.html' )

import datetime
def d_order_delivred(request):

    if request.method == "POST":
        order_id=request.POST.get("order_id")

        order=Order.objects.get(pk=order_id)
        if   order.is_accepted ==False or order.is_on_way ==False   :
         return redirect("active_order")
        
        else:
            order.is_delivered=True
            order.save()
            order.delivred_date=datetime.datetime.now()
            order.save()
            user=request.user
            user.deliver_num-=1
            user.save()

            wallet=user.wallet
            wallet.value+=order.restaurant.teslimat_ucreti
            wallet.save()
            wallet.value+=order.tip_value
            wallet.save()
            
            return redirect("active_order")
    return redirect("active_order")


from Jib.models import Wallet
def active_wallet(request):

    Wallet.objects.create(user=request.user)


    return redirect("deliver")

import io
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from django.shortcuts import render
from .models import Order
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64

import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def analyze_data(request):
    try:
        orders = Order.objects.all()

        restaurant_names = []
        total_prices = []
        created_at = []
        is_confirmed = []
        is_accepted = []
        is_delivered = []

        for order in orders:
            restaurant_names.append(order.restaurant.name)
            total_prices.append(order.total_price)
            created_at.append(order.created_at)
            is_confirmed.append(order.is_confirmed)
            is_accepted.append(order.is_accepted)
            is_delivered.append(order.is_delivered)

        unique_restaurants = list(set(restaurant_names))

        total_orders = []
        total_revenue = []
        confirmed_orders = []
        accepted_orders = []
        delivered_orders = []

        for restaurant in unique_restaurants:
            filtered_orders = [i for i in range(len(restaurant_names)) if restaurant_names[i] == restaurant]

            total_orders.append(len(filtered_orders))
            total_revenue.append(sum(total_prices[i] for i in filtered_orders))
            confirmed_orders.append(sum(is_confirmed[i] for i in filtered_orders))
            accepted_orders.append(sum(is_accepted[i] for i in filtered_orders))
            delivered_orders.append(sum(is_delivered[i] for i in filtered_orders))

        charts = {}

        def generate_chart(data, chart_type, title, x_label, y_label):
            fig, ax = plt.subplots(figsize=(10, 6))

            if chart_type == 'bar':
                ax.bar(data[0], data[1], color='teal')
            elif chart_type == 'line':
                ax.plot(data[0], data[1], color='blue')

            ax.set_title(title)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_xticklabels(data[0], rotation=45, ha='right')
            plt.tight_layout()

            img_stream = io.BytesIO()
            FigureCanvas(fig).print_png(img_stream)
            img_stream.seek(0)

            return img_stream

        total_revenue_chart = generate_chart(
            [unique_restaurants, total_revenue], 'bar', 
            "Restoran Başına Toplam Gelir", "Restoran", "Toplam Gelir (TL)"
        )
        charts['total_revenue'] = base64.b64encode(total_revenue_chart.getvalue()).decode('utf-8')

        total_orders_chart = generate_chart(
            [unique_restaurants, total_orders], 'bar', 
            "Restoran Başına Toplam Sipariş", "Restoran", "Toplam Siparişler"
        )
        charts['total_orders'] = base64.b64encode(total_orders_chart.getvalue()).decode('utf-8')

        x = np.arange(len(unique_restaurants))
        width = 0.35
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(x - width / 2, confirmed_orders, width, label='Onaylanmış Siparişler')
        ax.bar(x + width / 2, delivered_orders, width, label='Teslim Edilen Siparişler')
        ax.set_title("Restorana Göre Onaylanmış ve Teslim Edilmiş Siparişler")
        ax.set_xticks(x)
        ax.set_xticklabels(unique_restaurants, rotation=45, ha='right')
        ax.set_ylabel("Sipariş Sayısı")
        ax.legend()
        plt.tight_layout()

        img_stream = io.BytesIO()
        FigureCanvas(fig).print_png(img_stream)
        img_stream.seek(0)
        charts['confirmed_delivered_orders'] = base64.b64encode(img_stream.getvalue()).decode('utf-8')

        order_dates = sorted(set(created_at))

        daily_revenue = []
        for date in order_dates:
            revenue_for_day = sum(total_prices[i] for i in range(len(created_at)) if created_at[i].date() == date.date())
            daily_revenue.append(revenue_for_day)

        revenue_over_time_chart = generate_chart([order_dates, daily_revenue], 'line', 
                                                 "Zaman İçinde Gelir", "Tarih", "Gelir (TL)")
        charts['revenue_over_time'] = base64.b64encode(revenue_over_time_chart.getvalue()).decode('utf-8')

        context = {
            'restaurant_order_data': {
                'restaurant_names': unique_restaurants,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'confirmed_orders': confirmed_orders,
                'delivered_orders': delivered_orders,
            },
            'charts': charts
        }

        return render(request, 'restaurant_is_things/statistic.html', context)

    except Exception as e:
        print("Error in data analysis: ", str(e))
        return render(request, 'restaurant_is_things/statistic.html', context)

