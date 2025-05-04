from main import ConsistentHashRing

ring = ConsistentHashRing(virtual_nodes = 3)

ring.add_server("ServerA")
ring.add_server("ServerB")
ring.add_server("ServerC")

keys = ["user123", "order456", "session789", "profile000"]

for key in keys:
    ring.debug_key_mapping(key)


print("🧹 Removing ServerB...\n")
ring.remove_server("ServerB")

for key in keys:
    ring.debug_key_mapping(key)