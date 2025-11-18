import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from database import db, create_document, get_documents
from schemas import BreadProduct, Order, ContactMessage

app = FastAPI(title="Rasta Bread Man Company API", description="Backend for bakery website", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Rasta Bread Man Company API running"}


def _seed_products_if_empty():
    """Seed default bread products if collection is empty."""
    try:
        if db is None:
            return
        count = db["breadproduct"].count_documents({})
        if count == 0:
            defaults = [
                {
                    "name": "Chocolate Sweet Bread",
                    "description": "Rich, moist vegan loaf made with organic cacao and coconut sugar.",
                    "price": 8.5,
                    "flavor": "Chocolate",
                    "vegan": True,
                    "organic": True,
                    "image": "https://images.unsplash.com/photo-1541781286675-09d03b606ffa?q=80&w=1200&auto=format&fit=crop",
                    "in_stock": True,
                    "available_today": True,
                    "lead_time_hours": 0,
                    "is_special": False,
                    "special_price": None,
                    "tags": ["Customer Favorite"]
                },
                {
                    "name": "Banana Island Loaf",
                    "description": "Naturally sweet, ultra-soft banana bread with a hint of spice.",
                    "price": 7.5,
                    "flavor": "Banana",
                    "vegan": True,
                    "organic": True,
                    "image": "https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?q=80&w=1200&auto=format&fit=crop",
                    "in_stock": True,
                    "available_today": False,
                    "lead_time_hours": 24,
                    "is_special": True,
                    "special_price": 6.75,
                    "tags": ["Weekend Special", "Ripe Bananas"]
                },
                {
                    "name": "Coconut Sunshine Loaf",
                    "description": "Toasted coconut flakes and creamy coconut milk for a tropical treat.",
                    "price": 8.0,
                    "flavor": "Coconut",
                    "vegan": True,
                    "organic": True,
                    "image": "https://images.unsplash.com/photo-1548160-9c8b-4b57-9c1f-035e3e7d5b1e?q=80&w=1200&auto=format&fit=crop",
                    "in_stock": True,
                    "available_today": True,
                    "lead_time_hours": 0,
                    "is_special": False,
                    "special_price": None,
                    "tags": ["Toasted Coconut"]
                },
            ]
            for d in defaults:
                create_document("breadproduct", d)
    except Exception:
        # best-effort seeding; ignore errors so the endpoint still works
        pass


# Public endpoints
@app.get("/api/products", response_model=List[BreadProduct])
def list_products():
    try:
        _seed_products_if_empty()
        docs = get_documents("breadproduct")
        products = []
        for d in docs:
            d.pop("_id", None)
            products.append(BreadProduct(**d))
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/orders")
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        # Simulate sending notification (email/whatsapp) by acknowledging preference
        notify = {
            "channel": order.notify_via,
            "status": "queued"
        }
        return {"status": "ok", "order_id": order_id, "notification": notify}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def contact(message: ContactMessage):
    try:
        msg_id = create_document("contactmessage", message)
        return {"status": "ok", "message_id": msg_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
