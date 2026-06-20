from pydantic import BaseModel,Field,validator
from typing import Optional
# ⚠️ the lib below is  from motor lib as well to provide optional uuid for document _id in mongodb
from bson.objectid import ObjectId
class Project(BaseModel):
    
    _id: Optional[ObjectId]
    project_id: str = Field (..., min_length=1)
    
    # 👮 Custome field validation :: 
    @validator('project_id')
    def project_id_must_be_alpha_numeric(cls, value):
        if not value.isalnum():
            raise ValueError('Project ID must be alphanumeric')
        return value
    
    
    class Config:
        # Allow pydantic to ignore validation for arbitrary types like ObjectId ☝️ by overrding the config class of pydantic base model  
        arbitrary_types_allowed = True