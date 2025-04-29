# Docker Kurulumu

Bu dökümanda, Ubuntu sunucusuna Docker'ın nasıl kurulacağını adım adım açıklayacağız.

## Adım 1: Paketleri Güncelle
Sistemdeki paketleri güncelleyin:

```bash
sudo apt-get update
sudo apt-get install -y docker.io
```

## Adım 2: Docker Servisini Başlat
Kurulumdan sonra Docker servisini başlatmak ve otomatik açılmasını sağlamak için:

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## Adım 3: Kurulumu Doğrula
Docker'ın doğru çalıştığını doğrulamak için:

```bash
docker --version
```