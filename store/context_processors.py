from .models import Category,Product,Order,Customer

def categories(request):
    return{
        'categories': Category.objects.all()
    }