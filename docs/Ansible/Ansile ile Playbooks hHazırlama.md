# Nedir?

Ansible Playbook'ları, belirli bir iş akışını veya yapılandırma görevlerini tanımlamak için YAML formatında yazılan betiklerdir. Bu dosyalar, birden fazla görevi sırayla çalıştırarak sistemleri otomatik olarak yapılandırmayı ve yönetmeyi sağlar.

![0_ijjmn2cziz02b30a.png](https://secops.com.tr/0_ijjmn2cziz02b30a.png)

## Gereksinimler

-   Ansible kurulu Ubuntu Server (Tercihen latest vers)

## 1.Playbook ile Dosya Oluşturma

Şimdi her cihazda  **deneme.txt**  isminde bir dosya oluşturup içine bir mesaj yazan bir playbook hazırlayacağız.

Öncelikle  **/etc/ansible**  dizinine geçelim ve bir playbook dosyası oluşturalım:

```sh
cd /etc/ansible/
```


```sh
sudo nano create_file_playbook.yml
```


Dosyanın içeriği şu şekilde olacak:

```sh
---
- name: Create deneme text file  # Playbook'un adını belirler.
  hosts: all                     # Tüm envanterdeki sunuculara uygulanacağını belirtir.
  become: yes                    # Komutları root yetkileriyle çalıştırır.
  tasks:                          # Yapılacak görevleri tanımlayan blok.
    - name: Create deneme.txt in /tmp and write Emre  # Görevin adını belirler.
      copy:                        # 'copy' modülü kullanılır.
        content: "Emre"             # Dosyanın içine yazılacak içerik.
        dest: "/tmp/deneme.txt"     # Dosyanın oluşturulacağı tam yol (/tmp/deneme.txt).
        owner: root                 # Dosyanın sahibi root olacak.
        group: root                 # Dosyanın grubu root olacak.
        mode: '0644'                # Dosya izinleri.
```


Bu playbook, tüm hedef makinelerde  `/tmp/deneme.txt`  dosyasını oluşturup içine "Emre" yazacaktır.

Playbook'u çalıştırmak için şu komutu kullanabiliriz:

```sh
sudo ansible-playbook create_file_playbook.yml
```


Altta gördüğünüz gibi başarıyla sonuçlandı.

![playbook-cikti1.png](https://secops.com.tr/playbook-cikti1.png)

Biz genede işimizi sağlama alalım ve hedef makinelerin tmp dizini içerisinde oluşturalan deneme.txt dosyasını cat ile açalım. Yani şu komutu çalıştıralım:

```sh
sudo ansible all -m shell -a "cat /tmp/deneme.txt" -b
```


![playbook-cikti-2.png](https://secops.com.tr/playbook-cikti-2.png)

Yukarıda gördüğünüz çıktıda her makinenin ip adresinin altındaki Emre yazısı aslında bize  `/tmp/deneme.txt`  dosyasının içeriğini gösteriyor. Demek ki hedef dizinde dosyamız başarıyla oluşmuş ve içine istediğimiz şey yazılmış oldu.

