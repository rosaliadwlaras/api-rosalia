from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Data contoh untuk item skincare
item_skincare = [
     {"id": 1, "nama": "Hydrating Serum", "kategori": "Serum", "harga": 200, "tersedia": True, "jenis_kulit": ["Kering", "Normal"], "stok": 50},
    {"id": 2, "nama": "Brightening Cream", "kategori": "Krim", "harga": 300, "tersedia": True, "jenis_kulit": ["Semua"], "stok": 30},
    {"id": 3, "nama": "Brightening Cream", "kategori": "Tabir Surya", "harga": 150, "tersedia": True, "jenis_kulit": ["Semua"], "stok": 60},
    {"id": 4, "nama": "Anti-Aging Serum", "kategori": "Serum", "harga": 350, "tersedia": False, "jenis_kulit": ["Matang"], "stok": 0},
    {"id": 5, "nama": "Moisturizing Lotion", "kategori": "Losion", "harga": 180, "tersedia": True, "jenis_kulit": ["Berminyak", "Kombinasi"], "stok": 40}
]

# Fungsi untuk mendapatkan ID baru
def dapatkan_id_baru():
    if item_skincare:
        return max(item["id"] for item in item_skincare) + 1
    return 1

# Resource untuk daftar skincare
class DaftarSkincare(Resource):
    def get(self):
        """Mendapatkan daftar semua item skincare"""
        return {"error": False, "pesan": "berhasil", "jumlah": len(item_skincare), "items": item_skincare}

# Resource untuk menambahkan item skincare
class TambahSkincare(Resource):
    def post(self):
        """Menambahkan item skincare baru"""
        data = request.json
        id_baru = dapatkan_id_baru()
        
        item_baru = {
            "id": id_baru,
            "nama": data.get("nama"),
            "kategori": data.get("kategori"),
            "harga": data.get("harga"),
            "tersedia": data.get("tersedia", True),
            "jenis_kulit": data.get("jenis_kulit", ["Semua"]),
            "stok": data.get("stok", 0)
        }
        item_skincare.append(item_baru)
        
        return {"error": False, "pesan": "Item berhasil ditambahkan", "item": item_baru}, 201

# Resource untuk detail item skincare
class DetailSkincare(Resource):
    def get(self, id_item):
        """Mendapatkan detail item skincare berdasarkan ID"""
        item = next((item for item in item_skincare if item["id"] == id_item), None)
        if not item:
            return {"error": True, "pesan": "Item tidak ditemukan"}, 404
        return {"error": False, "pesan": "berhasil", "item": item}

# Resource untuk memperbarui item skincare
class PerbaruiSkincare(Resource):
    def put(self, id_item):
        """Memperbarui item skincare berdasarkan ID"""
        data = request.json
        item = next((item for item in item_skincare if item["id"] == id_item), None)
        if not item:
            return {"error": True, "pesan": "Item tidak ditemukan"}, 404
        
        # Memperbarui data item
        item.update({
            "nama": data.get("nama", item["nama"]),
            "kategori": data.get("kategori", item["kategori"]),
            "harga": data.get("harga", item["harga"]),
            "tersedia": data.get("tersedia", item["tersedia"]),
            "jenis_kulit": data.get("jenis_kulit", item["jenis_kulit"]),
            "stok": data.get("stok", item["stok"])
        })
        
        return {"error": False, "pesan": "Item berhasil diperbarui", "item": item}

# Resource untuk menghapus item skincare
class HapusSkincare(Resource):
    def delete(self, id_item):
        """Menghapus item skincare berdasarkan ID"""
        global item_skincare
        item_skincare = [item for item in item_skincare if item["id"] != id_item]
        
        return {"error": False, "pesan": "Item berhasil dihapus"}

# Registering resources with endpoints
api.add_resource(DaftarSkincare, "/skincare")  # Untuk GET daftar item skincare
api.add_resource(TambahSkincare, '/skincare/add')  # Untuk POST tambah item skincare
api.add_resource(DetailSkincare, "/skincare/<int:id_item>")  # Untuk GET detail item skincare
api.add_resource(PerbaruiSkincare, '/skincare/update/<int:id_item>')  # Untuk PUT perbarui item skincare
api.add_resource(HapusSkincare, '/skincare/delete/<int:id_item>')  # Untuk DELETE hapus item skincare

if __name__ == "__main__":
    app.run(debug=True)
