from django.db import migrations


CATEGORIES = [
    (
        "Soft Drinks",
        "soft-drinks",
        "Refreshing choices for everyday demand.",
        "Carbonated drinks and everyday refreshment for UAE trading businesses.",
        "photo-1622483767028-3f66f32aef97",
    ),
    (
        "Energy Drinks",
        "energy-drinks",
        "A category with energy.",
        "Discuss energy drink brands, formats and case requirements with our team. Product availability is confirmed for each enquiry.",
        "photo-1622543925917-763c34d1a86e",
    ),
    (
        "Juices",
        "juices",
        "Fruit-forward. Business-ready.",
        "Explore juice and fruit drink requirements, from individual servings to family formats. Tell us what your business needs.",
        "photo-1600271886742-f049cd451bba",
    ),
    (
        "Bottled Water",
        "bottled-water",
        "An everyday essential.",
        "Bottled drinking water requirements for trading companies across the UAE. Enquire with your preferred bottle sizes and case quantities.",
        "photo-1602143407151-7111542de6e8",
    ),
    (
        "Food & Groceries",
        "food-groceries",
        "Everyday pantry essentials.",
        "Food and grocery categories to complement your consumer goods requirements. Send your product list for a tailored discussion.",
        "photo-1542838132-92c53300491e",
    ),
    (
        "Laundry & Detergents",
        "laundry-detergents",
        "Care for the everyday.",
        "Laundry detergents and fabric care requirements for B2B trading. Specify brands, formats and packaging in your enquiry.",
        "photo-1582735689369-4fe89db7114c",
    ),
    (
        "Household Cleaning",
        "household-cleaning",
        "Essentials for cleaner spaces.",
        "Household cleaning goods for local trading businesses. Our team can discuss your category, packaging and quantity requirements.",
        "photo-1563453392212-326f5e854473",
    ),
    (
        "Cosmetics & Personal Care",
        "cosmetics-personal-care",
        "Daily care, thoughtfully sourced.",
        "Personal care and cosmetics requirements, alongside our wider consumer goods offering. Enquire about your preferred products and brands.",
        "photo-1608571423902-eed4a5ad8108",
    ),
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("catalogue", "Category")
    for order, (name, slug, short_description, description, photo) in enumerate(CATEGORIES):
        image_base = f"https://images.unsplash.com/{photo}?auto=format&fit=crop"
        Category.objects.get_or_create(
            slug=slug,
            defaults={
                "name": name,
                "short_description": short_description,
                "description": description,
                "hero_image_url": f"{image_base}&w=1600&q=85",
                "card_image_url": f"{image_base}&w=900&q=85",
                "sort_order": order,
                "featured": order < 4,
                "published": True,
                "seo_title": name,
                "seo_description": description,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("catalogue", "0001_initial")]

    operations = [migrations.RunPython(seed_categories, migrations.RunPython.noop)]
