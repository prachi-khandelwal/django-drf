# signals.py - Signal receivers for the products app

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver, Signal
from .models import Product
import logging
import uuid

# Get a logger for this module
logger = logging.getLogger('products')


# ==================== CUSTOM SIGNALS ====================
# Define custom signals for business-specific events

# Custom Signal: Fires when product stock goes low
product_low_stock = Signal()  # Create a new signal instance


# Signal Receiver 1: Auto-generate SKU and check stock before saving
@receiver(pre_save, sender=Product)
def generate_product_sku_and_check_stock(sender, instance, **kwargs):
    """
    This function is called BEFORE a Product is saved.
    1. Auto-generates a unique SKU if one doesn't exist
    2. Checks if stock is low and sends custom signal
    """
    # Part 1: Generate SKU if needed
    if not instance.sku:
        # Generate SKU: PROD-{short-uuid}
        short_uuid = str(uuid.uuid4())[:8].upper()
        instance.sku = f"PROD-{short_uuid}"
        logger.debug(f"🏷️  Auto-generated SKU: {instance.sku} for {instance.name}")
    
    # Part 2: Check for low stock and send custom signal
    LOW_STOCK_THRESHOLD = 10  # Alert when stock falls below 10
    
    if instance.stock < LOW_STOCK_THRESHOLD:
        # Send our custom signal!
        product_low_stock.send(
            sender=sender,
            product=instance,
            current_stock=instance.stock
        )


# Signal Receiver 2: Log product creation/updates
@receiver(post_save, sender=Product)
def log_product_save(sender, instance, created, **kwargs):
    """
    This function is called automatically after a Product is saved.
    It logs whether the product was created or updated.
    """
    if created:
        logger.info(f"✅ NEW PRODUCT CREATED: {instance.name} (ID: {instance.id}, SKU: {instance.sku}) by {instance.created_by}")
    else:
        logger.info(f"📝 PRODUCT UPDATED: {instance.name} (ID: {instance.id}, SKU: {instance.sku})")


# Signal Receiver 3: Before product deletion
@receiver(pre_delete, sender=Product)
def log_product_deletion_start(sender, instance, **kwargs):
    """
    This function is called BEFORE a Product is deleted.
    Use this to access data that will be gone after deletion.
    """
    logger.warning(f"⚠️  DELETING PRODUCT: {instance.name} (ID: {instance.id}, SKU: {instance.sku})")
    logger.info(f"   Stock at deletion: {instance.stock} units")
    logger.info(f"   Price at deletion: ${instance.price}")


# Signal Receiver 4: After product deletion
@receiver(post_delete, sender=Product)
def log_product_deletion_complete(sender, instance, **kwargs):
    """
    This function is called AFTER a Product is deleted.
    Use this for cleanup tasks (files, cache, etc.)
    """
    logger.info(f"🗑️  PRODUCT DELETED: {instance.name} (SKU: {instance.sku}) - Cleanup complete")
    # In real app, you might delete image files here:
    # if instance.image:
    #     instance.image.delete(save=False)


# ==================== CUSTOM SIGNAL RECEIVERS ====================

# Receiver for custom low stock signal
@receiver(product_low_stock)
def notify_low_stock(sender, product, current_stock, **kwargs):
    """
    This receiver is called when product_low_stock signal is sent.
    It logs a warning and could send email/SMS notifications.
    """
    logger.warning(f"🚨 LOW STOCK ALERT: {product.name} (SKU: {product.sku})")
    logger.warning(f"   Current stock: {current_stock} units - Reorder needed!")
    
    # In a real application, you might:
    # - Send email to inventory manager
    # - Create a purchase order
    # - Send SMS notification
    # - Update dashboard alert
    # send_email_to_manager(product, current_stock)
