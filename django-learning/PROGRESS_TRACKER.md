# Django REST API Learning Progress Tracker

**Last Updated:** 2025-12-12  
**Target:** 20 LPA Django Backend Developer Position  
**Current Progress:** ~98% Complete

---

## 📊 Progress Overview

```
██████████████████████████▓ 98% Complete
```

---

## ✅ COMPLETED TOPICS

### 1. Django Fundamentals ✅ 100%
- [x] Project setup with Poetry
- [x] Models (Product, ProductImage with relationships)
- [x] Database migrations
- [x] Admin interface
- [x] URL routing (app-level & project-level)
- [x] Django ORM basics (`.objects.all()`, `.filter()`, `.get()`)
- [x] Database indexes for optimization
- [x] Model Meta options (ordering, indexes)

### 2. Django REST Framework Basics ✅ 100%
- [x] DRF installation & configuration
- [x] Serializers (ProductSerializer with read-only fields)
- [x] `@api_view` decorator
- [x] Response objects with proper status codes
- [x] Professional error responses (status, message, errors, received_data)

### 3. CRUD Operations ✅ 100%
- [x] GET - Retrieve products (with filtering & pagination)
- [x] POST - Create products (with authentication)
- [x] PUT - Full update
- [x] PATCH - Partial update
- [x] DELETE - Delete products

### 4. Authentication ✅ 100%
- [x] User registration API
- [x] User login API
- [x] Token Authentication (DRF Token)
- [x] JWT Authentication setup (simplejwt configured)
- [x] `@permission_classes` decorator
- [x] `IsAuthenticated` permission

### 5. Custom Permissions ✅ 100%
- [x] `IsOwnerOrReadOnly` (object-level permission)
- [x] `IsAdminOrReadOnly` (admin moderation pattern)
- [x] `IsAdminOnly` (strict admin access)
- [x] Manual permission checking in function views
- [x] Understanding of `has_permission` vs `has_object_permission`

### 6. Query Features ✅ 100%
- [x] Manual pagination (page, page_size calculation)
- [x] DRF Pagination (PageNumberPagination)
- [x] Filtering (min_price, max_price, search)
- [x] Query parameters (`request.GET.get()`)
- [x] Pagination metadata in responses

### 7. User Relationships ✅ 100%
- [x] ForeignKey (created_by field)
- [x] User ownership validation
- [x] Owner-only modifications

### 8. ViewSets & Routers ✅ 100%
- [x] `ModelViewSet` implementation
- [x] `DefaultRouter` setup 
- [x] Automatic URL generation
- [x] `perform_create` override
- [x] Understanding function views vs ViewSets
- [x] Custom actions with `@action` decorator

### 9. Testing ✅ 100%
- [x] `APITestCase` setup
- [x] Model tests
- [x] API endpoint tests (GET, POST, PUT, PATCH, DELETE)
- [x] Authentication testing
- [x] Permission testing (owner vs non-owner)
- [x] Test coverage understanding

### 10. Error Handling ✅ 100%
- [x] Professional error responses
- [x] Validation error messages
- [x] Status codes (200, 201, 400, 401, 403, 404)
- [x] Detailed error information

### 11. Settings Configuration ✅ 100%
- [x] REST_FRAMEWORK settings
- [x] Pagination configuration
- [x] Authentication classes
- [x] JWT configuration
- [x] Logging setup

### 12. Advanced Serializers ✅ 100%
- [x] Nested serializers (UserSerializer, ProductImageSerializer)
- [x] `SerializerMethodField` (is_available, total_inv_val, formatted_price, image_url)
- [x] Custom validation (`validate_price`, `validate_stock`, `validate()`)
- [x] `to_representation()` understanding
- [x] Read-only vs write-only fields
- [x] Custom `create()` and `update()` methods
- [x] Object-level validation (multiple fields together)

### 13. Advanced Filtering ✅ 100%
- [x] `django-filter` package
- [x] FilterBackends (DjangoFilterBackend, SearchFilter, OrderingFilter)
- [x] Custom FilterSet class (ProductFilter)
- [x] SearchFilter with field prefixes (^name, description)
- [x] OrderingFilter with multiple fields
- [x] Replaced manual filtering with DRF filters

### 14. File Uploads ✅ 100%
- [x] ImageField configuration
- [x] Media files configuration (MEDIA_URL, MEDIA_ROOT)
- [x] Image serialization (ProductImageSerializer)
- [x] File validation (validate_image_file)
- [x] Multiple images per product (ProductImage model)
- [x] Custom upload action (`upload_image`)

### 15. Validators ✅ 100%
- [x] Custom field validators (validate_image_file)
- [x] XSS protection (validate_no_scripts)
- [x] File size validation
- [x] File type validation
- [x] Security validators

### 16. Database Optimization ✅ 100%
- [x] `select_related()` for ForeignKey optimization
- [x] `prefetch_related()` for reverse ForeignKey optimization
- [x] Database indexes (price, stock, created_at)
- [x] Composite indexes
- [x] Understanding N+1 query problem

### 17. Caching ✅ 100%
- [x] Cache configuration (LocMemCache)
- [x] Manual caching in views
- [x] Cache invalidation on create/update/delete
- [x] Cache keys management
- [x] View-level caching with `@method_decorator(cache_page)`
- [x] Custom statistics endpoint with caching

### 18. Throttling (Rate Limiting) ✅ 100%
- [x] Default throttling classes (AnonRateThrottle, UserRateThrottle)
- [x] Custom throttle classes (BurstRateThrottle, StrictAnonRateThrottle)
- [x] Throttle rates configuration
- [x] Action-specific throttling
- [x] Understanding rate limiting concepts

### 19. Security Settings ✅ 100% (Updated 2025-11-27)
- [x] XSS protection (SECURE_BROWSER_XSS_FILTER)
- [x] Content type sniffing protection (SECURE_CONTENT_TYPE_NOSNIFF)
- [x] Clickjacking protection (X_FRAME_OPTIONS)
- [x] HSTS configuration
- [x] Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- [x] HttpOnly cookies
- [x] SameSite cookie protection
- [x] Session configuration
- [x] Custom XSS validator (validate_no_scripts) applied to Product model
- [x] CSRF protection understanding
- [x] SQL injection protection (Django ORM)
- [x] Password security (built-in validators)

### 20. Debugging Tools ✅ 100%
- [x] Django Debug Toolbar setup
- [x] Logging configuration
- [x] Console and file logging
- [x] Debug logging for products app

### 21. Global Permission Strategy ✅ 100% (Updated 2025-11-28)
- [x] Understanding DEFAULT_PERMISSION_CLASSES concept
- [x] Implemented in settings.py (IsAuthenticatedOrReadOnly)
- [x] Tested with function views
- [x] Tested with ViewSets
- [x] Learned override patterns (more/less restrictive)
- [x] Created comprehensive examples file
- [x] Cleaned up redundant @permission_classes decorators

### 22. API Documentation ✅ 100% (Updated 2025-11-28)
- [x] drf-spectacular installation
- [x] Swagger UI setup (http://localhost:8000/api/docs/)
- [x] ReDoc setup (http://localhost:8000/api/redoc/)
- [x] Schema generation and configuration
- [x] Basic documentation with docstrings
- [x] Advanced documentation with @extend_schema
- [x] Response examples and tags
- [x] Understanding url_name parameter

### 23. CORS Configuration ✅ 100% (Updated 2025-11-28)
- [x] django-cors-headers installation
- [x] Added to INSTALLED_APPS and MIDDLEWARE
- [x] CORS_ALLOWED_ORIGINS configuration (localhost:3000, 5173, 8080)
- [x] CORS_ALLOW_CREDENTIALS setup
- [x] CORS_ALLOW_METHODS configuration
- [x] CORS_ALLOW_HEADERS configuration
- [x] Understanding CORS security (Same-Origin Policy)
- [x] Testing CORS with test HTML file
- [x] Production security best practices
- [x] Understanding who CORS affects (browsers vs mobile apps)

### 24. Environment Variables ✅ 100% (Updated 2025-11-28)
- [x] python-decouple installation with Poetry
- [x] .env file creation and configuration
- [x] SECRET_KEY, DEBUG, ALLOWED_HOSTS from environment
- [x] CORS_ALLOWED_ORIGINS from environment
- [x] Understanding config() and cast parameter
- [x] Using Csv() for comma-separated values
- [x] .gitignore setup to protect secrets
- [x] .env.example template creation
- [x] Environment-specific settings (dev vs production)
- [x] Security best practices for secret management

### 25. Production Settings ✅ 100% (Updated 2025-12-03)
- [x] PostgreSQL setup (flexible DB config with environment variables)
- [x] Static files configuration (STATIC_ROOT, collectstatic)
- [x] Security settings (auto-enable when DEBUG=False)
- [x] Production logging (environment-aware, separate error logs)
- [x] Error reporting (Sentry integration)
- [x] WhiteNoise understanding for static file serving

---

## ⬜ REMAINING TOPICS (Priority Order)

### Tier 2: Production-Ready Skills (~4-6 hours)

#### 26. Deployment ✅ 90%
- [x] Docker basics (images, containers, commands)
- [x] Dockerfile creation (multi-stage, ENV, COPY, RUN, CMD)
- [x] docker-compose setup (multi-container Django + PostgreSQL)
- [x] Gunicorn configuration (production WSGI server)
- [x] Nginx configuration (reverse proxy)
- [ ] Deploy to Heroku/Railway/Render
- [ ] CI/CD basics

#### 27. Advanced Topics (Optional) ⬜ 0%
- [ ] Celery for background tasks
- [ ] Redis for caching
- [ ] WebSockets (Django Channels)
- [ ] GraphQL (Graphene)
- [ ] API versioning

---

## 📝 NOTES & LEARNING INSIGHTS

### Key Concepts Mastered:
1. **View Hierarchy Understanding**: Function views → Generic views → ViewSets
2. **Permission System**: has_permission vs has_object_permission
3. **Query Optimization**: select_related vs prefetch_related
4. **Caching Strategy**: When to cache, when to invalidate
5. **Security First**: XSS, CSRF, HSTS, secure cookies

### Code Quality Improvements:
- Professional error responses
- Comprehensive validation
- Security-first approach
- Database optimization
- Clean code structure

### Interview-Ready Topics:
- ✅ Can explain DRF architecture
- ✅ Can implement custom permissions
- ✅ Can optimize database queries
- ✅ Can implement caching
- ✅ Can handle file uploads
- ✅ Can implement rate limiting
- ✅ Can configure security settings
- ✅ Can configure CORS for frontend integration
- ✅ Can configure production settings (DB, logging, error tracking)
- ✅ Can explain dev vs production differences
- ✅ Can Dockerize Django applications
- ✅ Can explain Docker concepts (images, containers, volumes)
- ✅ Can use docker-compose for multi-container setups
- ✅ Can configure Gunicorn for production
- ✅ Can configure Nginx as reverse proxy
- ✅ Can explain Nginx location blocks and proxy_pass

---

## 🎯 NEXT STEPS (Recommended Order)

1. **Deployment - Final Steps** (2-3 hours) ← IN PROGRESS
   - [ ] Deploy to Railway (cloud platform) ← START HERE
   - [ ] CI/CD basics (GitHub Actions)

2. **Advanced Topics** (Optional - 2-3 hours)
   - Celery for background tasks
   - API versioning
   - WebSockets basics

---


## 🔄 Update Log

- **2025-12-12**: Day 32 - Nginx Reverse Proxy (Complete)
  - Created nginx/nginx.conf configuration file
  - Learned upstream block (define backend servers)
  - Learned server block (listen port, server_name)
  - Learned location blocks (routing: /static/, /media/, /)
  - Configured proxy_pass and proxy headers (X-Real-IP, X-Forwarded-For)
  - Added Nginx service to docker-compose.yml
  - Configured shared volumes for static/media files
  - Successfully tested full stack: Nginx → Gunicorn → Django → PostgreSQL
  - Learned troubleshooting (ALLOWED_HOSTS, port binding)

- **2025-12-07**: Day 31 - Docker & Deployment (In Progress)
  - Learned Docker fundamentals (images, containers, layers)
  - Installed Colima (lightweight Docker alternative for Mac)
  - Created custom Dockerfile for Django
  - Configured Gunicorn as production server
  - Created docker-compose.yml for multi-container setup
  - Successfully ran Django + PostgreSQL in Docker
  - Learned docker exec, environment variables, volumes
  - Data persistence with named volumes

- **2025-12-03**: Day 30 - Production Settings (Complete)
  - Configured flexible database (SQLite dev / PostgreSQL production)
  - Added STATIC_ROOT for collectstatic command
  - Made security settings environment-aware (auto-enable on DEBUG=False)
  - Enhanced logging with separate error log files
  - Added Sentry error reporting integration
  - Learned WhiteNoise for static file serving
  - Created logs/ directory structure

- **2025-11-28**: Day 29 - Environment Variables (Complete)
  - Installed python-decouple package with Poetry
  - Created .env file for secret management
  - Updated settings.py to use config() for SECRET_KEY, DEBUG, ALLOWED_HOSTS
  - Moved CORS_ALLOWED_ORIGINS to environment variables
  - Learned config() function with cast parameter (bool, Csv)
  - Created .gitignore to protect .env from Git
  - Created .env.example template for team collaboration
  - Understood environment-specific settings (dev vs production)
  - Security best practices: Never commit secrets to Git

- **2025-11-28**: Day 28 - CORS Configuration (Complete)
  - Installed django-cors-headers package
  - Added corsheaders to INSTALLED_APPS
  - Added CorsMiddleware to MIDDLEWARE (before CommonMiddleware)
  - Configured CORS_ALLOWED_ORIGINS for dev (localhost:3000, 5173, 8080)
  - Set up CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
  - Created test_cors.html for browser testing
  - Learned CORS security best practices (production checklist)
  - Understood Same-Origin Policy and who CORS affects
  - Ready for frontend integration

- **2025-11-28**: Day 27 - API Documentation (Complete)
  - Installed and configured drf-spectacular
  - Set up Swagger UI at /api/docs/
  - Set up ReDoc at /api/redoc/
  - Added docstrings for basic documentation
  - Learned @extend_schema for advanced docs
  - Added response examples and tags
  - Learned step-by-step without overwhelming code dumps

- **2025-11-28**: Day 26 - Global Permission Strategy (Complete)
  - Implemented DEFAULT_PERMISSION_CLASSES in settings.py
  - Set IsAuthenticatedOrReadOnly as global default
  - Cleaned up redundant @permission_classes decorators
  - Learned override patterns (more/less restrictive)
  - Tested with ViewSets and function views
  - Created comprehensive permission examples file

- **2025-11-27**: Day 25 - Security (Enhanced)
  - Added custom XSS validator with regex patterns
  - Applied validators to Product model
  - Learned CSRF, SQL injection protection
  - Configured secure cookies (HttpOnly, SameSite)
  - Ready to move to Topic 21

- **2024-12-19**: Created progress tracker
  - Documented 20 completed topics
  - Identified 7 remaining topics
  - Set up tracking structure

---

## 💡 Tips for Success

1. **Focus on understanding, not memorization**
2. **Build projects to reinforce concepts**
3. **Practice explaining concepts out loud**
4. **Review completed topics regularly**
5. **Test everything you build**

---

## 📚 Resources Reference

- Django REST Framework Docs: https://www.django-rest-framework.org/
- Django Security: https://docs.djangoproject.com/en/stable/topics/security/
- DRF Filtering: https://www.django-rest-framework.org/api-guide/filtering/
- DRF Permissions: https://www.django-rest-framework.org/api-guide/permissions/

---

**Remember:** This tracker is a living document. Update it as you complete topics!

