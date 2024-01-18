from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routes.address import address_router
from routes.cart import cart_router
from routes.image import image_router
from routes.item import item_router
from routes.order import order_router
from routes.review import review_router
from routes.shop import shop_router
from routes.user import user_router
from routes.wishlist import wishlist_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/", response_model=dict)
async def root() -> dict:
    return {"Hello": "World"}


app.include_router(address_router)
app.include_router(cart_router)
app.include_router(image_router)
app.include_router(item_router)
app.include_router(order_router)
app.include_router(review_router)
app.include_router(shop_router)
app.include_router(user_router)
app.include_router(wishlist_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8888, reload=True)
