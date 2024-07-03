# app/schemas.py
from typing import List
from .models import EconomiaBase, OccupazioneBase, ProduttivitaBase

class EconomiaResponse(EconomiaBase):
    pass

class OccupazioneResponse(OccupazioneBase):
    pass

class ProduttivitaResponse(ProduttivitaBase):
    pass

class EconomiaListResponse(BaseModel):
    data: List[EconomiaResponse]

class OccupazioneListResponse(BaseModel):
    data: List[OccupazioneResponse]

class ProduttivitaListResponse(BaseModel):
    data: List[ProduttivitaResponse]