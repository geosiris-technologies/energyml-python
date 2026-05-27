import json
from typing import List, Dict
from energyml.resqml.v2_0_1.resqmlv2 import ResqmlPropertyKind
from energyml.utils.epc_utils import __CACHE_PROP_KIND_DICT__, get_property_kind_by_title

def title_inclusion(t0: str, t1: str) -> bool:
    t0_words = set(t0.lower().split())
    t1_words = set(t1.lower().split())
    return t0_words.issubset(t1_words) or t1_words.issubset(t0_words)
    

def search_matching_title(title: List[str]) -> Dict[str, List[str]]:
    potential_matches = {t: [] for t in title}
    for pk in __CACHE_PROP_KIND_DICT__.values():
        for t in title:
            if title_inclusion(t, pk.citation.title):
                potential_matches[t].append(pk.citation.title)
    return potential_matches

if __name__ == "__main__":
    not_found = []
    for p in ResqmlPropertyKind:
        print(p)
        pk = get_property_kind_by_title(p.value)
        if pk is None:
            not_found.append(p.value)
        print(f"\t{pk.uuid}" if pk is not None else "\tNot found")
        
    
    print("Not found tried to match:")
    matches = search_matching_title(not_found)
    for title, matched_titles in matches.items():
        print(f"\t{title}: ")
        for mt in matched_titles:
            print(f"\t\t{mt}")
            
    with open("pk_not_found_matches.json", "w") as f:
        json.dump(matches, f, indent=4)
