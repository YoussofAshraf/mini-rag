from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId

class dataChunk(BaseModel):
    _id : Optional[ObjectId]
    chunk_text:str =Field(..., min_length=1)
    chunk_metadata: dict = Field(...)
    chunk_order:int = Field(..., gt=0) # gt = > 'greater than'
    
    
    class Config:
        arbitrary_types_allowed = True
