
# app/models.py
from pydantic import BaseModel
from typing import Optional

class EconomiaBase(BaseModel):
    anno: int
    regione: str
    valore_aggiunto: float

class OccupazioneBase(BaseModel):
    anno: int
    regione: str
    occupazione: int

class ProduttivitaBase(BaseModel):
    anno: int
    regione: str
    produttivita: float
