from app.services.vector_store_service import get_collection

collection = get_collection()

print("Collection:", collection.name)
print("Number of documents:", collection.count())

results = collection.get()

print("\nIDs:")
print(results["ids"])

print("\nMetadata:")
print(results["metadatas"])

print("\nFirst document:")
print(results["documents"][0][:300])