"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Bakery-specific schemas

class BreadProduct(BaseModel):
    """
    Bread products offered by the bakery
    Collection name: "breadproduct"
    """
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Short product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    flavor: Literal["Chocolate", "Banana", "Coconut"] = Field(..., description="Bread flavor")
    vegan: bool = Field(True, description="Whether the bread is vegan")
    organic: bool = Field(True, description="Whether ingredients are organic")
    image: Optional[str] = Field(None, description="Image URL for the product")
    in_stock: bool = Field(True, description="Whether currently in stock")

class Order(BaseModel):
    """
    Customer orders
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    email: EmailStr = Field(..., description="Customer email")
    phone: Optional[str] = Field(None, description="Customer phone number")
    product_name: str = Field(..., description="Name of the bread product")
    quantity: int = Field(1, ge=1, le=50, description="Quantity ordered")
    notes: Optional[str] = Field(None, description="Special instructions")

class ContactMessage(BaseModel):
    """
    General contact messages or inquiries
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    message: str = Field(..., min_length=5, max_length=2000, description="Message contents")

# Example schemas kept for reference (not used by app directly)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
