# Pemrograman Jaringan Tugas 2

**Deskripsi:**

Buatlah sebuah program time server dengan ketentuan sebagai berikut:

a. Membuka port di port 45000 dengan transport TCP

b. Server harus dapat melayani request yang concurrent, gunakan contoh multithreading

c. Ketentuan request yang dilayani:

- Diawali dengan string “TIME dan diakhiri dengan karakter 13 dan karakter 10”

- Setiap request dapat diakhiri dengan string “QUIT” yang diakhiri dengan karakter 13 dan 10

d. Server akan merespon dengan jam dengan ketentuan:

- Dalam bentuk string (UTF-8)

- Diawali dengan “JAM<spasi><jam>”

- "jam" berisikan info jam dalam format “hh:mm:ss” dan diakhiri dengan karakter 13 dan karakter 10

![hasil](https://github.com/danielcristho/netpro-2/assets/69733783/b1e2261e-7b61-4916-bb27-9886ebfd4af1)
