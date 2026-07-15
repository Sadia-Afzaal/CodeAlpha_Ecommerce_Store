from .models import Category


def categories(request):
    """Make the category list available to every template (nav / footer)."""
    return {"nav_categories": Category.objects.all()}
