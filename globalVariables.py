"""Tady se ukládají globální porměnné."""
# tréninky v databázi nejsou indexované, ale při každém spuštění souboru se každému tréninku jeden index přiřadí, 
#aby se s nimi dalo dle potřeby nakládat
# index tréninku
training_id = 0
# metoda pro zvyšování id 
def increaseID (id : int) -> int:
    """Metoda zvýší id tréninku o 1."""
    return id + 1