from dataclasses import dataclass

@dataclass
class Retailer:
    Retailer_code: int
    Retailer_name: str
    Type: str
    Country: str


    def __hash__(self):
        return self.codice

    def __eq__(self, other):
        return self.codice == other.codice
