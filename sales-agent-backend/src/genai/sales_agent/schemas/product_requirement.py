from pydantic import BaseModel, Field

class ProductRequirementSchema(BaseModel):
    """Product Requirement Schema."""

    requirement: str = Field(..., description="Yêu cầu về sản phẩm của User")
    category: str = Field(..., description="Loại sản phẩm")
    price_condition: str = Field(..., description="Điều kiện giá sản phẩm của User")
