from fastapi import FastAPI
from routers import usuarios, quadras, agendamentos
app = FastAPI()

app.include_router(usuarios.router)
app.include_router(quadras.router)
app.include_router(agendamentos.router)
