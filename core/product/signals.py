from components.general.caching.delete_cache_keys import delete_keys_with_prefix
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from product.models import Product, ProductType, PriceCurrency


@receiver(post_save, sender=Product)
def product_clear_cache_post_save(sender, instance: Product, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('product', pk=pk)


@receiver(post_delete, sender=Product)
def product_clear_cache_post_delete(sender, instance: Product, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('product', pk=pk)


@receiver(post_save, sender=ProductType)
def product_type_clear_cache_post_save(sender, instance: ProductType, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('product_type', pk=pk)


@receiver(post_delete, sender=ProductType)
def product_type_clear_cache_post_delete(sender, instance: ProductType, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('product_type', pk=pk)


@receiver(post_save, sender=PriceCurrency)
def price_currency_clear_cache_post_save(sender, instance: PriceCurrency, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('price_currency', pk=pk)


@receiver(post_delete, sender=PriceCurrency)
def price_currency_clear_cache_post_delete(sender, instance: PriceCurrency, **kwargs) -> None:
    pk = instance.id if instance.id else ''
    delete_keys_with_prefix('price_currency', pk=pk)
