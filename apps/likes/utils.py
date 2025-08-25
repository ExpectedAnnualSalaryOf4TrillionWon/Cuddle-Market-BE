from apps.likes.models import ProductLike

def get_like_count(product_id: int) -> int:
    """특정 상품의 찜 개수 반환"""
    return ProductLike.objects.filter(product_id=product_id).count()