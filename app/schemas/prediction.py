from pydantic import BaseModel, Field


class HouseFeatures(BaseModel):
    """Input schema for Boston Housing prediction request."""

    crim: float = Field(..., json_schema_extra={"example": 0.02729})
    zn: float = Field(..., json_schema_extra={"example": 0.0})
    indus: float = Field(..., json_schema_extra={"example": 7.07})
    chas: int = Field(..., json_schema_extra={"example": 0})
    nox: float = Field(..., json_schema_extra={"example": 0.469})
    rm: float = Field(..., json_schema_extra={"example": 7.185})
    age: float = Field(..., json_schema_extra={"example": 61.1})
    dis: float = Field(..., json_schema_extra={"example": 4.9671})
    rad: int = Field(..., json_schema_extra={"example": 2})
    tax: int = Field(..., json_schema_extra={"example": 242})
    ptratio: float = Field(..., json_schema_extra={"example": 17.8})
    black: float = Field(..., json_schema_extra={"example": 392.83})
    lstat: float = Field(..., json_schema_extra={"example": 4.03})


class PredictionResponse(BaseModel):
    """Output schema for prediction response."""

    request_id: str
    predicted_medv: float
    stored: bool


class HealthResponse(BaseModel):
    status: str
    model_exists: bool


class DbHealthResponse(BaseModel):
    status: str
    database: str
