from pydantic import BaseModel, Field
from typing import Optional

# Pydantic models are like Django/DRF Serializers or Django Forms
# They define the data schema, types, and validation rules

class ScanResult(BaseModel):
    """
    Defines the structure for a successful scan submission response
    
    This model ensures that our API always returns data in this format and is used by
    FastApi to auto-generate API documentation
    
    """
    # 'Field' allows adding metadata, like examples for the documentation
    scan_id: str = Field(..., example='a1b2c3d4...')
    resource: str = Field(..., example='f1e2d3c4...')
    response_code: int = Field(example=1)
    verbose_msg: str = Field(example='Scan request successfully queued, come back for the report')
    permalink: Optional[str] = Field(default=None, example='https://www.virustotal.com/...')
    
    # This config tells Pydantic to expect a dictionary (not an object attribute)
    class Config:
        from_attributes = True

class ScanError(BaseModel):
    """
    Defines the structure for a failed scan submission
    """
    detail: str = Field(example='Scan request failed, check resource and try again')