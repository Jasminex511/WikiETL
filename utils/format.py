from pydantic import BaseModel, field_validator
from datetime import datetime
import re

class person(BaseModel):
    name: str
    spouse: str | None
    birthdate: str
    nationality: str
    keywords: str

    @field_validator('birthdate')
    def validate_birthdate(cls, v):
        bc_pattern = r'^(\d+)-BC$'
        negative_date_pattern = r'^-\d{4}-\d{2}-\d{2}$'
        
        if re.match(negative_date_pattern, v):
            return v
            
        if re.match(bc_pattern, v):
            year = int(re.match(bc_pattern, v).group(1))
            return f"-{year:04d}-01-01"
        
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            if v.isdigit():
                return f"{v}-01-01"
            raise ValueError('Invalid birthdate format. Please use YYYY-MM-DD or YYYY-BC for ancient dates.')
