# 🚁 Drone Filo Optimizasyonu Projesi

Bu proje, çok sayıda dronun teslimat görevlerini en verimli şekilde planlamak için geliştirilen algoritmaların performansını karşılaştırmayı amaçlamaktadır. Farklı senaryolarda A*, CSP + A* ve Genetik Algoritma (GA) yöntemleri kullanılarak rota optimizasyonu yapılmıştır.

---

## 🎯 Proje Amacı

Günümüzde drone teknolojisi, lojistik ve teslimat hizmetlerinde önemli bir yer tutmaktadır. Bu projede, drone filosunun teslimat rotalarını; enerji tüketimi, teslimat başarı oranı, batarya şarj süreleri ve işlem süresi gibi kritik kriterlere göre optimize ederek, gerçek dünya koşullarına uygun hale getirmek hedeflenmiştir.

---

## 🛠️ Kullanılan Algoritmalar

- **A\***  
  En kısa yol algoritmasıdır. Basit ve küçük ölçekli senaryolarda hızlı sonuç verir.

- **CSP + A\***  
  Kısıt Programlama (Constraint Satisfaction Problem) ile zaman pencereleri ve uçuş kısıtları dahil edilerek A* algoritmasıyla rota planlanmasını sağlar.

- **Genetik Algoritma (GA)**  
  Evrimsel yöntemler kullanarak karmaşık ve büyük veri setlerinde yüksek başarı ve optimizasyon sağlamaya çalışır.

---

## 📊 Veri Setleri ve Senaryolar

- **Sabit Veri Seti:**  
  Önceden tanımlanmış 5 drone, 20 teslimat noktası ve öncelikler içeren, kısıtsız ve statik ortam.

- **Dinamik Veri Seti:**  
  Rastgele oluşturulmuş teslimat noktaları, no-fly zone (uçuş yasağı alanları), zaman pencereleri ve değişken önceliklerle daha gerçekçi ve karmaşık ortamlar.

---

## ⚙️ Operasyonel Kısıtlar

- 🔋 **Batarya Limiti:**  
  Drone bataryası %30’un altına inerse, 20 dakika boyunca şarj olur.

- ⏰ **Zaman Penceresi:**  
  Teslimatlar belirlenen zaman aralığına uygun yapılmalıdır; aksi takdirde geçersiz sayılır.

- ⚠️ **Öncelik Bazlı Ceza:**  
  Düşük öncelikli teslimatlarda ceza uygulanır:  
  `Ceza = (6 - Öncelik) × 100`

- 📦 **Min-Heap Kullanımı:**  
  Teslimatlar, önceliğe göre Min-Heap yapısı ile sıralanır ve işlenir.

---

## 📈 Performans Kriterleri

- ✅ **Başarı Oranı:**  
  Kurallara uygun tamamlanan teslimatların yüzdesi.

- 🔌 **Enerji Tüketimi:**  
  Toplam rota mesafesi ve yük taşıma enerjisi baz alınarak hesaplanır.

- ⏳ **Çözüm Süresi:**  
  Algoritmanın rota planlaması için geçen süre (saniye).

- 🏆 **Skor:**  
  Teslimat başarısı, enerji tüketimi ve şarj sürelerinin dengelenmiş toplam performans değeri:  
  `Skor = (Başarılı Teslimat Sayısı × 100) - Toplam Enerji - Toplam Şarj Süresi`

---

## 📝 Sonuçlar ve Değerlendirme

- 🚀 **A\*** algoritması, küçük ve basit senaryolarda hızlı ve etkili sonuçlar sunar.

- ⚖️ **CSP + A\***, zaman pencereleri ve uçuş kısıtları içeren senaryolarda dengeli ve uygulanabilir çözümler üretir.

- 🧬 **Genetik Algoritma (GA)**, karmaşık ve büyük ölçekli senaryolarda yüksek başarı ve performans sağlar ancak işlem süresi daha uzundur.

---

![SABİT VERİ senaryo0](https://github.com/user-attachments/assets/6b77fb11-f3a2-4d30-87ef-2196d411cc2a)


**Sabit Veriyle Tüm Algoritma Testleri**
#
![DİNAMİK VERİ senaryo1](https://github.com/user-attachments/assets/1b8b471d-03de-4484-97a9-8b4929667b8b)


**Dinamik Veriyle Tüm Algoritma Testleri**
#
![DİNAMİK VERİ senaryo2](https://github.com/user-attachments/assets/8bd9c2ed-75a1-4d1e-aba3-16679656d6f9)



**Dinamik Veriyle 10 drone, 50 teslimat Senaryosu**
#
![senaryo3](https://github.com/user-attachments/assets/0eb578bb-c992-4431-a75a-f36397e187d9)



**Dinamik Veriyle Min-Heap kullanarak öncelikli teslimatları sıralama Senaryosu**
#
