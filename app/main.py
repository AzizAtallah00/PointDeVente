from fastapi import FastAPI
from app.routers import employee, session, customer, category, product

app = FastAPI()

app.include_router(employee.router)
app.include_router(session.router)
app.include_router(customer.router)
app.include_router(category.router)
app.include_router(product.router)



