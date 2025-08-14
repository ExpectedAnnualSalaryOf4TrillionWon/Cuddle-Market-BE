from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Product

User = get_user_model()


class ProductModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_product_creation(self):
        product = Product.objects.create(
            user=self.user,
            title="Test Product",
            description="Test description",
            price=10000,
            category="food",
            condition_status="new",
            trade_method="direct",
            location="Seoul",
        )
        self.assertEqual(product.title, "Test Product")
        self.assertEqual(product.price, 10000)
        self.assertFalse(product.is_deleted)

    # def test_product_like_unique_constraint(self):
    #     product = Product.objects.create(
    #         user=self.user,
    #         title="Test Product 2",
    #         description="Test description",
    #         price=15000,
    #         category="toy",
    #         condition_status="used",
    #         trade_method="delivery",
    #         location="Busan",
    #     )
    #     like1 = ProductLike.objects.create(user=self.user, product=product)
    #     with self.assertRaises(Exception):
    #         # 동일 사용자가 같은 상품 찜 두번 하면 에러 발생
    #         like2 = ProductLike.objects.create(user=self.user, product=product)
