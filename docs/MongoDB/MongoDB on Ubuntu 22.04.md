# Installing MongoDB on Ubuntu 22.04 and SetUp

## Prerequisites
MongoDB'yi kuralım:
-   Ubuntu Server 22.04 LTS
-   Root or sudo privileges
-   Good internet connection

Update the system package list:
```bash
sudo apt update
```
Import the MongoDB public GPG key:
```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc  | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/mongodb-6.gpg
```

Add the MongoDB repository
```bash
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```
Update the package list again:
```bash
sudo apt update
```
Install MongoDB:
```bash
sudo apt install mongodb-org  
```
Start and enable MongoDB to run on boot:
```bash
sudo systemctl enable --now mongod
```
## Step 2: Configure MongoDB Users and Authentication

Open the MongoDB shell:
```bash
mongosh
```
Create a root user:
```sql
use admin  
db.createUser({  
  user: "root",  
  pwd: "rootpassword",  
  roles: ["root"]  
})
```
Create a new user and add them to a database:
```sql
use yourDatabase  
db.createUser({  
  user: "yourUser",  
  pwd: "userPassword",  
  roles: [{ role: "readWrite", db: "yourDatabase" }]  
})
```
Enable authentication by editing the MongoDB configuration file  `/etc/mongod.conf`  and uncommenting the  `security`  section:

## Step 1: Create a Key File for MongoDB Authentication

Generate a Key File: This key file will be used for internal authentication between replica set members or sharded cluster components. You can generate a key file using the following command:
```bash
openssl rand -base64 756 > /etc/mongodb-keyfile
```
Set Appropriate Permissions: The key file must have read permissions for the MongoDB user and should be owned by the MongoDB user. You can set the appropriate permissions with:
```bash
sudo chown mongodb:mongodb /etc/mongodb-keyfile 
```
```bash 
sudo chmod 400 /etc/mongodb-keyfile
```
## Step 2: Configure MongoDB to Use the Key File and Enable Authentication

1.  Edit the MongoDB Configuration File: Open the  `/etc/mongod.conf`  file in your favorite text editor:
```bash
sudo nano /etc/mongod.conf
```
Enable Authentication and Specify the Key File: In the  `mongod.conf`  file, you'll need to uncomment (or add if not present) the  `security`  section and add the  `keyFile`  directive under it. You should also ensure that the  `authorization`  option is enabled:
```bash
security:  
  authorization: enabled  
  keyFile: /etc/mongodb-keyfile
```
1.  This configuration enables client authentication, requiring users to log in, and also configures the MongoDB instance to use the specified key file for internal authentication.
2.  Restart MongoDB: After making these changes, save the file and restart MongoDB to apply the new configuration:
```bash
sudo systemctl restart mongod
```
## Step 3: Set Up Replication

Edit the  `/etc/mongod.conf`  file to configure replication: (use nano  `/etc/mongod.conf)`
```bash
replication:  
  replSetName: "rs0"
```
Restart MongoDB:
```bash
sudo systemctl restart mongod
```
Connect to the MongoDB shell and initiate the replica set:
```bash
mongosh  
rs.initiate()
```
Add another server to the replica set (replace  `otherServerAddress`  with the actual address)
```bash
rs.add("otherServerAddress")
```
otherServerAddress is another server where monogdb installed

## Secure MongoDB with SSL and Domain

## Option A: Using Let’s Encrypt (for production)

Install Certbot:
```bash
sudo apt install certbot
```
Obtain a certificate (ensure your domain is pointing to your server):
```bash
sudo certbot certonly --standalone -d mongo-db.example.com
```
our certificates will be stored in  `/etc/letsencrypt/live/mongo-db.example.com/`. You'll primarily need  `fullchain.pem`  and  `privkey.pem`.

## Option B: Generating Self-Signed Certificates (for testing)

Generate a new private key and certificate:
```bash
openssl req -newkey rsa:4096 -nodes -keyout mongodb.key -x509 -days 365 -out mongodb.crt
```
Combine the key and certificate into a  `.pem`  file:
```bash
cat mongodb.crt mongodb.key > mongodb.pem
```
Secure the permissions for your  `.pem`  file:
```bash
chmod 600 mongodb.pem
```
## Configure MongoDB to Use TLS/SSL

## Step 1: Prepare the MongoDB Configuration

Concatenate the Certificate and Key: MongoDB expects the SSL certificate and key in a single file for its configuration. You can concatenate your  `fullchain.pem`  and  `privkey.pem`  into a single  `.pem`  file using the following command:
```bash
cat /etc/letsencrypt/live/mongodbserver.example.com/fullchain.pem /etc/letsencrypt/live/mongodbserver.example.com/privkey.pem > /etc/ssl/mongodb.pem
```
Secure the Permissions: Ensure that the concatenated file is readable by the MongoDB process, which typically runs as the  `mongodb`  user:
```bash
sudo chown mongodb:mongodb /etc/ssl/mongodb.pem  
```
```bash
sudo chmod 600 /etc/ssl/mongodb.pem
```
## Step 2: Configure MongoDB to Use TLS/SSL

Edit the MongoDB Configuration File: Open the MongoDB configuration file, usually located at  `/etc/mongod.conf`, with your preferred text editor:
```bash
sudo nano /etc/mongod.conf
```
Add TLS/SSL Configuration: In the  `mongod.conf`  file, add or modify the  `net`  section to include the path to your concatenated  `.pem`  file and enable TLS:
```bash
net:  
  tls:  
    mode: requireTLS  
    certificateKeyFile: /etc/ssl/mongodb.pem
```
1.  This configuration forces MongoDB to use TLS for all connections and specifies the certificate and key file to use.
2.  Restart MongoDB: Apply the changes by restarting the MongoDB service:
```bash
sudo systemctl restart mongod
```
## Step 3: Verify the Configuration

1.  Check MongoDB Logs: Look at the MongoDB logs to ensure there are no errors related to the TLS configuration. The logs are typically located at  `/var/log/mongodb/mongod.log`.
2.  Connect with TLS Enabled: Try connecting to your MongoDB server using the  `mongosh`  client with TLS enabled to verify the setup:
```bash
mongosh --tls --host mongodbserver.example.com
```
## Additional Considerations

-   Firewall and Network Security: Ensure that your firewall rules are configured to allow traffic on the MongoDB port (default is 27017) only from trusted sources.
-   Regularly Renew Certificates: Let’s Encrypt certificates are valid for 90 days. Set up a cron job or use a Certbot timer to automatically renew your certificates.
-   Backup Configuration: Always keep a backup of your configuration files and certificates in a secure location.

## Configure MongoDB to Use the Key File and Enable Authentication

Edit the MongoDB Configuration File: Open the  `/etc/mongod.conf`  file in your favorite text editor:
```bash
sudo nano /etc/mongod.conf
```
Enable Authentication and Specify the Key File: In the  `mongod.conf`  file, you'll need to uncomment (or add if not present) the  `security`  section and add the  `keyFile`  directive under it. You should also ensure that the  `authorization`  option is enabled:
```bash
security:  
  authorization: enabled  
  keyFile: /etc/mongodb-keyfile
```
1.  This configuration enables client authentication, requiring users to log in, and also configures the MongoDB instance to use the specified key file for internal authentication.
2.  Restart MongoDB: After making these changes, save the file and restart MongoDB to apply the new configuration:
```bash
sudo systemctl restart mongod
```
## Step 3: Verify the Configuration

-   Verify Authentication is Required: Try connecting to your MongoDB instance without credentials to ensure that authentication is now required:
```bash
mongosh
```
Now you can get A Secured Monogdb Cluster on Your Ubuntu Server make sure give right firewall config.
