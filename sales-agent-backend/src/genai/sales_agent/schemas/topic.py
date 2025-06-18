from pydantic import BaseModel, Field

class TopicSchema(BaseModel):
    """Topic schema."""

    name: str = Field(..., description="Một trong các giá trị sau: greeting, off_topic, company_info, product_qna, make_order")
    confidence: float = Field(..., description="Score between 0 and 1")
    context: str = Field(..., description="User's input")