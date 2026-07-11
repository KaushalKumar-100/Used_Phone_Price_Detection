from pydantic import BaseModel

class PredictionRequest(BaseModel):
    brand: str
    model: str
    release_year: int
    ram_gb: int
    storage_gb: int
    screen_size_inches: float
    battery_capacity: int
    processor_score: int
    camera_score: int
    os_type: str
    has_5g: int
    original_price: int
    purchase_year: int
    age_months: int
    usage_hours_per_day: float
    condition: str
    battery_health: int
    screen_cracked: int
    body_damage: int
    repair_history: int
    water_damage: int
    warranty_remaining_months: int
    box_available: int
    charger_available: int
    market_demand_score: int
class PredictionResponse(BaseModel):
    
    prediction:float
    