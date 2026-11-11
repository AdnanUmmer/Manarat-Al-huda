"""Presentation groups for existing records. Uploaded images always take precedence."""
from django.templatetags.static import static

BEVERAGES = ("soft-drinks", "energy-drinks", "bottled-water", "juices")
ASSETS = {
    "soft-drinks": "softdrinks", "energy-drinks": "energy", "bottled-water": "water",
    "juices": "juices", "food-groceries": "food", "laundry-detergents": "cleaning",
    "household-cleaning": "cleaning", "cosmetics-personal-care": "cosmetics",
}

def catalogue_groups(categories):
    drinks = [row for row in categories if row.slug in BEVERAGES]
    # Give Soft Drinks the lead slot, respecting admin order among the remaining cards.
    drinks.sort(key=lambda row: row.slug != "soft-drinks")
    return {"beverages": drinks, "other_categories": [row for row in categories if row.slug not in BEVERAGES]}

def image_path(slug, width):
    key = ASSETS.get(slug)
    return static(f"images/categories/{key}-{width}.webp") if key else ""

