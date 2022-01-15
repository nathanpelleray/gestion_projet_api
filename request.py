from pydantic import BaseModel
"""
{
  "switch1": "null",
  "switch2": "on",
  "switch3": "null",
  "range1": "82",
  "range2": "100",
  "range3": "16",
  "range4": "0.5"
}
"""
class Request(BaseModel):
    switch1: str
    switch2: str
    switch3: str
    range1: str
    range2: str
    range3: str
    range4: str
