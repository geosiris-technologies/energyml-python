# Benchmark de performance pour get_obj_uuid
import time
import re
from types import SimpleNamespace

UUID_RGX: re.Pattern = re.compile(r"[Uu]u?id|UUID")


# Version originale
def get_obj_uuid_original(obj):
    try:
        return getattr(obj, "uuid", None) or getattr(obj, "uid")
    except AttributeError:
        if isinstance(obj, dict):
            for k in obj.keys():
                if UUID_RGX.match(k):
                    return obj[k]
    return None


# Version optimisée
def get_obj_uuid_fast(obj):
    for attr in dir(obj):
        if UUID_RGX.match(attr):
            value = getattr(obj, attr, None)
            if value is not None:
                return value
    if isinstance(obj, dict):
        for k, v in obj.items():
            if UUID_RGX.match(k):
                if v is not None:
                    return v
    return None


# Simulation d'une classe TriangulatedSetRepresentation
class TriangulatedSetRepresentation:
    def __init__(self, uuid):
        self.uuid = uuid


N = 10000
objs = [TriangulatedSetRepresentation(f"uuid-{i}") for i in range(N)]

# Test version originale
start = time.perf_counter()
for obj in objs:
    assert get_obj_uuid_original(obj) == obj.uuid
elapsed_original = time.perf_counter() - start

# Test version optimisée
start = time.perf_counter()
for obj in objs:
    assert get_obj_uuid_fast(obj) == obj.uuid
elapsed_fast = time.perf_counter() - start

print(f"Original version: {elapsed_original:.6f} s for {N} calls")
print(f"Optimized version: {elapsed_fast:.6f} s for {N} calls")
