from hash_file import get_hash

class ConsistentHashRing:
    def __init__(self , virtual_nodes=3):
        self.virtual_nodes = virtual_nodes
        self.ring = dict()
        self.sorted_hashes = []

    def add_server(self , server_name: str):
        for i in range(self.virtual_nodes):
            vnode_name = f"{server_name}-VN{i}"
            print(f"vnode_name : {vnode_name}")
            h = get_hash(vnode_name)
            print(f"{server_name} : hash  - {h}")
            self.ring[h] = server_name
            print(f"ring : {self.ring}")
            self.sorted_hashes.append(h)
            print(f"sorted_hashes array : {self.sorted_hashes}")

    def remove_server(self, server_name: str):
        to_remove = []
        for h in self.sorted_hashes:
            if self.ring[h] == server_name:
                to_remove.append(h)

        for h in to_remove:
            del self.ring[h]
            self.sorted_hashes.remove(h)

    def get_server(self , key:str) -> str:
        h = get_hash(key)
        for node_hash in self.sorted_hashes:
            if h <= node_hash:
                return self.ring[node_hash]
        return self.ring[self.sorted_hashes[0]]

    def debug_key_mapping(self , key:str):
        key_hash = get_hash(key)

        print(f"\n🔑 Key: '{key}'")
        print(f"   → Hashed to        : {key_hash}")  

        for h in self.sorted_hashes:
            print(f"   Ring Node Hash     : {h} → Server: {self.ring[h]}")  

        server = self.get_server(key)
        for h in self.sorted_hashes:
            if key_hash <= h:
                print(f"   → Mapped to Server : {self.ring[h]} (via hash {h})")
                break
        else:
            print(f"   → Mapped to Server : {self.ring[self.sorted_hashes[0]]} (wrapped around)")
        print()
