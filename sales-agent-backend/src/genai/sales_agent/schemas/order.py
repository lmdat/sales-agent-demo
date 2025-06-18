from pydantic import BaseModel, Field


class OrderItemSchema(BaseModel):
    """Order Item Schema."""

    product_name: str = Field(..., description="Tên sản phẩm mà User muốn mua")
    category: str = Field(..., description="Loại sản phẩm")
    sku: str = Field(..., description="Mã sản phẩm mà User muốn mua")
    ordered_qty: int = Field(..., description="Số lượng của từng sản phẩm mà User muốn mua")
    price: float = Field(..., description="Giá của từng sản phẩm mà User muốn mua")
    
class OrderInfoSchema(BaseModel):
    """Order Info Schema."""

    customer_name: str = Field(..., description="Họ tên của User")
    customer_phone: str = Field(..., description="Số phone của User")
    customer_email: str = Field(..., description="Email của User")
    customer_address: str = Field(..., description="Địa chỉ của User")
    delivery_type: str = Field(..., description="Phương thức giao hàng")
    order_confirmation: str = Field(..., description="User đồng ý xác nhận thông tin đơn hàng.")
    order_items: list[OrderItemSchema] = Field(..., description="Danh sách sản phẩm mà User muốn mua")
    

    