from pydantic import BaseModel, Field


class UsageTokensSchema(BaseModel):
    """Usage Tokens Schema."""

    input: int = Field(..., description="Input tokens")
    output: int = Field(..., description="Output tokens")
    total: int = Field(..., description="Total tokens")