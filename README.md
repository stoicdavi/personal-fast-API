# DevOps Stage 1 — FastAPI + Nginx

A simple FastAPI backend deployed behind an Nginx reverse proxy on AWS EC2.

---

## API Endpoints

| Method | Path | Response |
|--------|------|----------|
| GET | `/` | `{"message": "API is running"}` |
| GET | `/health` | `{"message": "healthy"}` |
| GET | `/me` | Personal details |

---

## Part 1: Run Locally

**Prerequisites:** Python 3.8+

```bash
git clone https://github.com/yourusername/personal-fast-API.git
cd personal-fast-API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit: `http://127.0.0.1:8000`

---

## Part 2: Deploy on AWS (Ubuntu + Nginx + Systemd)

### Step 1 — Launch EC2 Instance

- AMI: Ubuntu 22.04 LTS
- Create a key pair
- Subnet: Public subnet with **Auto-assign public IP** enabled
- Security Group inbound rules:

| Port | Protocol | Source |
|------|----------|--------|
| 22 | TCP | Your IP (or `0.0.0.0/0`) |
| 80 | TCP | `0.0.0.0/0` |

---

### Step 2 — Initial SSH Access

```bash
ssh -i "your-key.pem" ubuntu@<your_public_ip>
```

---

### Step 3 — Create a Dedicated User

```bash
sudo adduser hngdevops
sudo usermod -aG sudo hngdevops
```

Allow passwordless sudo:

```bash
sudo visudo
```

Add at the bottom:

```
hngdevops ALL=(ALL) NOPASSWD:ALL
```

---

### Step 4 — Configure SSH for the New User

```bash
sudo su - hngdevops
mkdir ~/.ssh && chmod 700 ~/.ssh
sudo cp /home/ubuntu/.ssh/authorized_keys ~/.ssh/
sudo chown hngdevops:hngdevops ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
exit
```

---

### Step 5 — Harden SSH

```bash
sudo nano /etc/ssh/sshd_config
```

Set:

```
PermitRootLogin no
PasswordAuthentication no
```

```bash
sudo systemctl restart sshd
```

---

### Step 6 — Install Dependencies

Log in as the new user:

```bash
ssh -i "your-key.pem" hngdevops@<your_public_ip>
```

Install packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip nginx git -y
```

---

### Step 7 — Clone & Set Up the App

```bash
git clone https://github.com/yourusername/personal-fast-API.git
cd personal-fast-API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

### Step 8 — Create a Systemd Service

```bash
sudo nano /etc/systemd/system/fastapi.service
```

```ini
[Unit]
Description=Uvicorn instance to serve FastAPI
After=network.target

[Service]
User=hngdevops
Group=www-data
WorkingDirectory=/home/hngdevops/personal-fast-API
Environment="PATH=/home/hngdevops/personal-fast-API/.venv/bin"
ExecStart=/home/hngdevops/personal-fast-API/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl start fastapi
sudo systemctl enable fastapi
```

Verify it's running:

```bash
sudo systemctl status fastapi
```

---

### Step 9 — Configure Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/fastapi
```

```nginx
server {
    listen 80;
    server_name <your_public_ip_or_domain>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the config:

```bash
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

---

### Step 10 — Access the API

Open your browser or run:

```bash
curl http://<your_public_ip>/
curl http://<your_public_ip>/health
curl http://<your_public_ip>/me
```
