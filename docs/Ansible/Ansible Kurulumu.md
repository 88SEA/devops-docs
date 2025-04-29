
## Ansible Kurulumu

Öncelikle Ansible'nin en son latest versiyonunu  [buradaki](https://github.com/ansible/ansible)  github adresinden öğrenebilirsiniz.

-   Kuruluma başlamak için öncelikle yerel paketlerinizi güncelleyin ve yükseltin.

```
sudo apt update && sudo apt upgrade
```
software-properties-common reposunu kurun:

```
sudo apt install software-properties-common
```

Ansible'in resmi PPA deposunu sisteminize ekleyin:

```
sudo add-apt-repository --yes --update ppa:ansible/ansible
```

Ansible'i kurun:

```
sudo apt install ansible
```

Kurulumun başarılı olduğunu kontrol etmek için, Ansible sürümünü kontrol edin:

```
ansible --version
```


Bu komut çıktısı olarak Ansible'ın en son sürümünü göstermelidir.
