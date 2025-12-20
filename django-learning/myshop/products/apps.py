from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self):
        """
        This method is called when Django starts.
        We import signals here to register them.
        """
        import products.signals  # noqa