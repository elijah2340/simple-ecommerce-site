from .models import Category


def menulinks(request):
    links = Category.objects.all()
    return dict(links=links)
