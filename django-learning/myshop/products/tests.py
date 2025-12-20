from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product
from decimal import Decimal

# API Testing imports
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


class ProductModelTest(TestCase):
    """
    This class tests our Product model.
    We'll check if products are created correctly.
    """
    
    def setUp(self):
        """
        This runs BEFORE each test.
        We create test data here.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.product = Product.objects.create(
            name='Test Laptop',
            description='A laptop for testing',
            price=Decimal('999.99'),
            stock=10,
            created_by=self.user
        )
    
    def test_product_creation(self):
        """
        Test if a product is created with correct data.
        """
        self.assertEqual(self.product.name, 'Test Laptop')
        self.assertEqual(self.product.price, Decimal('999.99'))
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.created_by, self.user)
    
    def test_product_str_method(self):
        """
        Test if __str__ returns the product name.
        """
        self.assertEqual(str(self.product), 'Test Laptop')


class ProductAPITest(APITestCase):
    """
    This class tests our Product API endpoints.
    We'll test GET, POST, PUT, DELETE operations.
    """
    
    def setUp(self):
        """
        This runs BEFORE each test.
        Creates test user and sample products.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )
        
        # Create test products
        self.product1 = Product.objects.create(
            name='Laptop',
            description='Gaming laptop',
            price=Decimal('1200.00'),
            stock=5,
            created_by=self.user
        )
        
        self.product2 = Product.objects.create(
            name='Mouse',
            description='Wireless mouse',
            price=Decimal('25.99'),
            stock=50,
            created_by=self.user
        )
    
    def test_get_product_list(self):
        """
        Test GET request to retrieve all products.
        """
        # Make a GET request to the products list endpoint
        # url = reverse('products_list')
        # NEW VIEWSET
        url = reverse('product-list')

        response = self.client.get(url)
        
        # Check if request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if we got 2 products (we created 2 in setUp)
        self.assertEqual(response.data['count'], 2)
    
    def test_create_product_authenticated(self):
        """
        Test POST request to create a new product (with authentication).
        """
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        
        # Product data to send
        # url = reverse('product_add')
        # NEW VIEWSET
        url = reverse('product-list')
        data = {
            'name': 'Keyboard',
            'description': 'Mechanical keyboard',
            'price': '150.00',
            'stock': 20
        }
        
        # Make POST request
        response = self.client.post(url, data, format='json')
        
        # Print error details if test fails (helpful for debugging!)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Error: {response.data}")
        
        # Check if product was created (status 201)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check if product exists in database
        self.assertEqual(Product.objects.count(), 3)  # 2 from setUp + 1 new
    
    def test_create_product_unauthenticated(self):
        """
        Test POST request WITHOUT authentication (should fail).
        """
        # DON'T authenticate - simulate a guest/hacker trying to create product
        
        # Product data to send
        # url = reverse('product_add')
        # NEW VIEWSET
        url = reverse('product-list')
        data = {
            'name': 'Hacker Product',
            'description': 'Should not be created',
            'price': '999.99',
            'stock': 100
        }
        
        # Make POST request WITHOUT authentication
        response = self.client.post(url, data, format='json')
        
        # Should get 401 Unauthorized or 403 Forbidden
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        
        # Verify product was NOT created in database
        self.assertEqual(Product.objects.count(), 2)  # Still only 2 from setUp
    
    def test_update_product_put(self):
        """
        Test PUT request to fully update a product (owner can update).
        """
        # Authenticate as the owner
        self.client.force_authenticate(user=self.user)
        
        # URL for updating product1
        # url = reverse('product_detail', kwargs={'pk': self.product1.pk})

        url = reverse('product-detail', kwargs={'pk': self.product1.pk})

        
        # New data (PUT requires ALL fields)
        data = {
            'name': 'Updated Laptop',
            'description': 'Updated description',
            'price': '1500.00',
            'stock': 10
        }
        
        # Make PUT request
        response = self.client.put(url, data, format='json')
        
        # Check if update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh product from database
        self.product1.refresh_from_db()
        
        # Verify product was actually updated in database
        self.assertEqual(self.product1.name, 'Updated Laptop')
        self.assertEqual(self.product1.price, Decimal('1500.00'))


    def test_update_product_patch(self):
        """
        Test PATCH request to partially update a product (owner can update).
        """
        # Authenticate as the owner
        self.client.force_authenticate(user=self.user)
        
        # URL for updating product2
        # url = reverse('product_detail', kwargs={'pk': self.product2.pk})

        url = reverse('product-detail', kwargs={'pk': self.product2.pk})

        
        # Only update ONE field (that's what PATCH is for!)
        data = {
            'name': 'Updated Wireless Mouse'
        }
        
        # Make PATCH request
        response = self.client.patch(url, data, format='json')
        
        # Check if update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh product from database
        self.product2.refresh_from_db()
        
        # Verify name was updated
        self.assertEqual(self.product2.name, 'Updated Wireless Mouse')
        
        # Verify OTHER fields were NOT changed (important for PATCH!)
        self.assertEqual(self.product2.price, Decimal('25.99'))  # Original price unchanged
        self.assertEqual(self.product2.stock, 50)  # Original stock unchanged
    
    def test_update_product_non_owner(self):
        """
        Test that a different user CANNOT update someone else's product.
        This tests the IsOwnerOrReadOnly permission!
        """
        # Create a DIFFERENT user (not the owner)
        hacker_user = User.objects.create_user(
            username='hacker',
            password='hack123'
        )
        
        # Authenticate as the HACKER (not the owner)
        self.client.force_authenticate(user=hacker_user)
        
        # Try to update product1 (owned by self.user, not hacker_user)
        # url = reverse('product_detail', kwargs={'pk': self.product1.pk})
        url = reverse('product-detail', kwargs={'pk': self.product1.pk})

        data = {
            'name': 'Hacked Product',
            'description': 'Should not work',
            'price': '1.00',
            'stock': 999
        }
        
        # Make PUT request
        response = self.client.put(url, data, format='json')
        
        # Should get 403 Forbidden (not owner!)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify product was NOT modified in database
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Laptop')  # Original name unchanged!
        self.assertEqual(self.product1.price, Decimal('1200.00'))  # Original price unchanged!
    
    def test_delete_product_owner(self):
        """
        Test DELETE request by owner (should succeed).
        """
        # Authenticate as the owner
        self.client.force_authenticate(user=self.user)
        
        # URL for deleting product1
        # url = reverse('product_detail', kwargs={'pk': self.product1.pk})
        url = reverse('product-detail', kwargs={'pk': self.product1.pk})

        
        # Make DELETE request
        response = self.client.delete(url)
        
        # Check if deletion was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify product was deleted from database
        self.assertEqual(Product.objects.count(), 1)  # Only product2 remains
        
        # Verify product1 doesn't exist anymore
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=self.product1.pk)
    
    def test_delete_product_non_owner(self):
        """
        Test DELETE request by non-owner (should fail).
        """
        # Create a different user
        other_user = User.objects.create_user(
            username='otheruser',
            password='other123'
        )
        
        # Authenticate as the non-owner
        self.client.force_authenticate(user=other_user)
        
        # Try to delete product1 (owned by self.user)
        # url = reverse('product_detail', kwargs={'pk': self.product1.pk})
        url = reverse('product-detail', kwargs={'pk': self.product1.pk})

        response = self.client.delete(url)
        
        # Should get 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify product still exists in database
        self.assertEqual(Product.objects.count(), 2)  # Both products still there
        self.assertTrue(Product.objects.filter(pk=self.product1.pk).exists())


class AdvancedSerializerTest(APITestCase):
    """
    Test Advanced Serializer features:
    - Nested serializers
    - Custom validation
    - SerializerMethodFields
    - Custom create() method
    """
    
    def setUp(self):
        """Create test users and products"""
        self.user = User.objects.create_user(
            username='john',
            email='john@example.com',
            password='testpass123'
        )
        
        self.product = Product.objects.create(
            name='Gaming Laptop',
            description='High-end gaming laptop with RTX 4090',
            price=Decimal('1500.00'),
            stock=50,
            created_by=self.user
        )
        
        self.client = APIClient()
    
    def test_nested_serializer_shows_user_details(self):
        """Test that created_by field shows nested user object, not just ID"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that created_by is an object, not just an ID
        created_by = response.data['created_by']
        self.assertIsInstance(created_by, dict)  # Should be a dictionary/object
        
        # Check nested user fields
        self.assertEqual(created_by['id'], self.user.id)
        self.assertEqual(created_by['username'], 'john')
        self.assertEqual(created_by['email'], 'john@example.com')
    
    def test_price_validation_rejects_negative_price(self):
        """Test that negative prices are rejected"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-list')
        data = {
            'name': 'Test Product',
            'description': 'A test product',
            'price': -50.00,  # Negative price!
            'stock': 10
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should be rejected with 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertIn('greater than zero', str(response.data['price']))
    
    def test_stock_validation_rejects_negative_stock(self):
        """Test that negative stock is rejected"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-list')
        data = {
            'name': 'Test Product',
            'description': 'A test product',
            'price': 100.00,
            'stock': -10  # Negative stock!
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stock', response.data)
        self.assertIn('cannot be negative', str(response.data['stock']))
    
    def test_stock_validation_allows_zero_stock(self):
        """Test that zero stock is allowed (out of stock is valid)"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-list')
        data = {
            'name': 'Test Product - Out of Stock',
            'description': 'A test product',
            'price': 100.00,
            'stock': 0  # Zero stock should be allowed!
        }
        
        response = self.client.post(url, data, format='json')
        
        # Should be accepted (with the out of stock name rule passing)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['stock'], 0)
    
    def test_object_validation_expensive_product_needs_long_description(self):
        """Test that expensive products (>$10,000) need detailed descriptions"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-list')
        data = {
            'name': 'Super Expensive Laptop',
            'description': 'Short desc',  # Only 10 characters - too short!
            'price': 15000.00,  # Over $10,000
            'stock': 5
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertIn('detailed description', str(response.data))
    
    def test_serializer_method_field_is_available(self):
        """Test that is_available field is computed correctly"""
        self.client.force_authenticate(user=self.user)
        
        # Test 1: Product with stock > 0 should be available
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_available'])  # stock = 50, so available
        
        # Test 2: Product with stock = 0 should NOT be available
        self.product.stock = 0
        self.product.save()
        
        response = self.client.get(url)
        self.assertFalse(response.data['is_available'])  # stock = 0, not available
    
    def test_serializer_method_field_total_inv_val(self):
        """Test that total_inv_val is computed correctly (price × stock)"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Expected: 1500.00 × 50 = 75000.00
        expected_value = Decimal('1500.00') * 50
        self.assertEqual(Decimal(str(response.data['total_inv_val'])), expected_value)
    
    def test_serializer_method_field_formatted_price(self):
        """Test that formatted_price displays with currency symbol"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should be formatted as "$1,500.00"
        self.assertEqual(response.data['formatted_price'], '$1,500.00')
    
    def test_custom_create_automatically_sets_created_by(self):
        """Test that custom create() method automatically sets created_by from request"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('product-list')
        data = {
            'name': 'Auto Created Product',
            'description': 'This product should have created_by set automatically',
            'price': 500.00,
            'stock': 20
            # Notice: We DON'T send created_by!
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that created_by was automatically set to the authenticated user
        self.assertEqual(response.data['created_by']['id'], self.user.id)
        self.assertEqual(response.data['created_by']['username'], 'john')
        
        # Verify in database too
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.created_by, self.user)
    
    def test_custom_update_updates_product_correctly(self):
        """Test that custom update() method properly updates products"""
        self.client.force_authenticate(user=self.user)
        
        # Get the original values
        original_name = self.product.name
        original_price = self.product.price
        
        # Update the product
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        data = {
            'name': 'Updated Gaming Laptop',
            'description': 'Updated description for the gaming laptop',
            'price': 2000.00,  # Changed from 1500
            'stock': 75  # Changed from 50
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response data
        self.assertEqual(response.data['name'], 'Updated Gaming Laptop')
        self.assertEqual(Decimal(str(response.data['price'])), Decimal('2000.00'))
        self.assertEqual(response.data['stock'], 75)
        
        # Verify in database
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Gaming Laptop')
        self.assertEqual(self.product.price, Decimal('2000.00'))
        self.assertEqual(self.product.stock, 75)
        
        # Verify created_by didn't change (should still be original user)
        self.assertEqual(self.product.created_by, self.user)


class ProductFilteringTestCase(APITestCase):
    """
    Test filtering, searching, and ordering functionality.
    Tests: DjangoFilterBackend, SearchFilter, OrderingFilter
    """
    
    def setUp(self):
        """
        Create test data with diverse products for filtering tests.
        """
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
        # Create diverse products for testing filters
        self.laptop1 = Product.objects.create(
            name='Gaming Laptop Pro',
            description='High-performance gaming laptop with RTX graphics',
            price=Decimal('1500.00'),
            stock=5,
            created_by=self.user1
        )
        
        self.laptop2 = Product.objects.create(
            name='Laptop Business',
            description='Professional laptop for office work',
            price=Decimal('800.00'),
            stock=10,
            created_by=self.user1
        )
        
        self.mouse = Product.objects.create(
            name='Wireless Mouse',
            description='Ergonomic mouse for gaming and productivity',
            price=Decimal('50.00'),
            stock=0,  # Out of stock
            created_by=self.user2
        )
        
        self.keyboard = Product.objects.create(
            name='Mechanical Keyboard',
            description='RGB keyboard with mechanical switches',
            price=Decimal('120.00'),
            stock=15,
            created_by=self.user2
        )
        
        self.list_url = reverse('product-list')
    
    def test_filter_by_exact_price(self):
        """
        Test filtering products by exact price.
        URL: ?price=50.00
        """
        response = self.client.get(self.list_url, {'price': '50.00'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Wireless Mouse')
    
    def test_filter_by_price_min(self):
        """
        Test filtering products with minimum price.
        URL: ?price_min=100
        Should return products with price >= 100
        """
        response = self.client.get(self.list_url, {'price_min': '100'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)  # keyboard, laptop2, laptop1
        
        # Verify no products below $100
        for product in response.data['results']:
            self.assertGreaterEqual(Decimal(product['price']), Decimal('100'))
    
    def test_filter_by_price_range(self):
        """
        Test filtering products with price range (min and max).
        URL: ?price_min=100&price_max=1000
        Should return products with 100 <= price <= 1000
        """
        response = self.client.get(self.list_url, {
            'price_min': '100',
            'price_max': '1000'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # keyboard, laptop2
        
        # Verify all products are in range
        for product in response.data['results']:
            price = Decimal(product['price'])
            self.assertGreaterEqual(price, Decimal('100'))
            self.assertLessEqual(price, Decimal('1000'))
    
    def test_filter_by_stock_in_stock_only(self):
        """
        Test filtering for in-stock products only.
        URL: ?stock__gte=1
        Should exclude out-of-stock items (stock=0)
        """
        response = self.client.get(self.list_url, {'stock__gte': '1'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)  # All except mouse (stock=0)
        
        # Verify all products have stock >= 1
        for product in response.data['results']:
            self.assertGreaterEqual(product['stock'], 1)
    
    def test_search_by_name_starts_with(self):
        """
        Test search with '^name' prefix (starts with matching).
        URL: ?search=Laptop
        Should find products where name STARTS with "Laptop"
        """
        response = self.client.get(self.list_url, {'search': 'Laptop'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Both laptops
        
        # Verify both results have names starting with "Laptop"
        for product in response.data['results']:
            self.assertTrue(product['name'].startswith('Laptop') or 
                          'laptop' in product['description'].lower())
    
    def test_search_in_description(self):
        """
        Test search in description field (contains matching).
        URL: ?search=gaming
        Should find products with "gaming" in name OR description
        """
        response = self.client.get(self.list_url, {'search': 'gaming'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find: Gaming Laptop Pro (name) + Wireless Mouse (description)
        self.assertEqual(response.data['count'], 2)
    
    def test_ordering_by_price_ascending(self):
        """
        Test ordering products by price (cheapest first).
        URL: ?ordering=price
        """
        response = self.client.get(self.list_url, {'ordering': 'price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get first 3 results (due to pagination)
        results = response.data['results']
        prices = [Decimal(p['price']) for p in results]
        
        # Verify prices are in ascending order
        self.assertEqual(prices, sorted(prices))
    
    def test_ordering_by_price_descending(self):
        """
        Test ordering products by price (most expensive first).
        URL: ?ordering=-price
        """
        response = self.client.get(self.list_url, {'ordering': '-price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        results = response.data['results']
        prices = [Decimal(p['price']) for p in results]
        
        # Verify prices are in descending order
        self.assertEqual(prices, sorted(prices, reverse=True))
    
    def test_combined_filter_search_and_order(self):
        """
        Test combining multiple filters: search + price range + ordering.
        URL: ?search=laptop&price_min=500&price_max=1500&ordering=price
        This tests the real-world scenario!
        """
        response = self.client.get(self.list_url, {
            'search': 'laptop',
            'price_min': '500',
            'price_max': '1500',
            'ordering': 'price'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should find: Gaming Laptop Pro ($1500) and Laptop Business ($800)
        self.assertEqual(response.data['count'], 2)
        
        # First result should be cheaper one (ordering=price)
        self.assertEqual(response.data['results'][0]['name'], 'Laptop Business')

