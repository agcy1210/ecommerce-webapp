from shop.models import Product
from django.conf import settings
from decimal import Decimal

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        #getting the current cart using session id
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        #if there is no previous cart then creating one
        self.cart = cart

    #cart = {product_id:{'quantity':__,'price':__}}

    def add(self, product, quantity=1, update_quantity=False):
        #product id is converted to string as per JSON format
        product_id = str(product.id)
        #if the given product is not available in cart then add it
        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0, 'price':str(product.price)}
        #if product is there in cart the update the quantity
        if update_quantity:
            self.cart[product_id]['quantity']=quantity
        #increment the product quantity which is present in cart using id
        else:
            self.cart[product_id]['quantity']+=quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID]=self.cart
        self.session.modified = True

    def remove(self):
        product_id = str(product.id)
        #check if product is there or not
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        #get all the keys
        product_ids = self.cart.keys()
        #get all the products using keys
        products = Product.objects.filter(id__in=product_ids)
        #iterate through products
        for product in products:
            self.cart[str(product.id)]['product']=product
        #iterate and set price and total_price values
        for item in self.cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['quantity']*item['price']
            yield item

    def __len__(self):
        #get the no of items in cart
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        #get the total price of the items in cart
        return sum(Decimal(item['price']*item['quantity'] for item in self.cart.values()))

    def clear(self):
        #to clear the contents of cart say clear cart session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


