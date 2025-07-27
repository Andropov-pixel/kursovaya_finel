from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dependencies.database import get_async_session
from dependencies.fastapi_users_instance import fastapi_users, get_jwt_strategy
from products.models import Product
from products.schemas import ProductCreate, ProductRead, ProductUpdate

products_router = APIRouter(tags=["Products"])
current_user = fastapi_users.current_user()

@products_router.post("/create_product", dependencies=[Depends(current_user)], response_model=ProductCreate)
async def create_product(product: ProductCreate, user=Depends(current_user),
                         db: AsyncSession = Depends(get_async_session)):
    print(user)
    if current_user.role == "admin":
        db_product = Product(**product.model_dump())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product
    else:
        return JSONResponse(
            content={"detail": "You don`t have enough permissions."},
            status_code=status.HTTP_403_FORBIDDEN,
        )


@products_router.get("/get_product", response_model=ProductRead)
async def get_product(id_product: int, db: AsyncSession = Depends(get_async_session),
                      user=Depends(current_user)):
    result = await db.execute(select(Product).where(Product.id == id_product))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.patch("/update_product", response_model=ProductUpdate)
async def update_product(
        id_product: int,
        product_update: ProductUpdate,
        db: AsyncSession = Depends(get_async_session),
        user=Depends(current_user)
):
    result = await db.execute(select(Product).where(Product.id == id_product))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    await db.commit()
    await db.refresh(product)
    return product


@products_router.delete("/delete_product")
async def delete_product(id_product: int, db: AsyncSession = Depends(get_async_session),
                         user=Depends(current_user)):
    result = await db.execute(select(Product).where(Product.id == id_product))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(product)
    await db.commit()
    return JSONResponse(
        content={"detail": "Product deleted successfully."},
        status_code=status.HTTP_200_OK,
    )