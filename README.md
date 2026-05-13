# Turing Makinesi ile Binary Çarpma Simülasyonu

Bu proje, iki binary sayıyı "Shift and Add" algoritmasını kullanarak çarpan bir Turing Makinesi simülasyonudur.

## Çalışma Mantığı
Program, kullanıcıdan alınan iki binary sayıyı bir bant (tape) üzerine yerleştirir ve şu durumları simüle eder:
- **q0:** Çarpma işaretini (`*`) bulana kadar ilerler.
- **q1:** Çarpan sayının bitlerini kontrol eder.
- **q2/q3:** 0 veya 1 bit değerine göre kaydırma ve toplama işlemlerini gerçekleştirir. Bu durumlar işlem sırasını takip ederek ('=') işaretini görene kadar bant üzerinde hareket etmeye devam eder.
- **q_accept:** Sonucu bant üzerine yazar ve işlemi tamamlar.
