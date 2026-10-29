"""Melihat tokenizer IndoBERT memecah teks (EKSPERIMEN BERAT: butuh transformers; mengunduh berkas tokenizer kecil)."""
import sys

from transformers import AutoTokenizer

NAMA_MODEL = sys.argv[1] if len(sys.argv) > 1 else "indobenchmark/indobert-base-p1"

# --8<-- [start:muat]
tokenizer = AutoTokenizer.from_pretrained(NAMA_MODEL)
print("model:", NAMA_MODEL, "| ukuran kosakata:", tokenizer.vocab_size)
# --8<-- [end:muat]

# --8<-- [start:pecah]
contoh = [
    "Tolong, air banjir sudah masuk ke rumah kami.",
    "Banjirnya tinggi bgt, toloooong!",
    "Saya sedang membaca berita tentang gempa tahun lalu.",
]
for teks in contoh:
    kode = tokenizer(teks)
    print("\nteks      :", teks)
    print("token     :", tokenizer.convert_ids_to_tokens(kode["input_ids"]))
    print("jumlah id :", len(kode["input_ids"]))
# --8<-- [end:pecah]

# --8<-- [start:batch]
batch = tokenizer(contoh, padding=True, truncation=True, max_length=32, return_tensors="pt")
print("\nbentuk input_ids :", tuple(batch["input_ids"].shape))
print("attention_mask[0]:", batch["attention_mask"][0].tolist())
# --8<-- [end:batch]
