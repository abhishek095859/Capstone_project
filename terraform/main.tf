provider "aws" {
  region  = "ap-south-1"
  profile = "my-sso"
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_security_group" "monitoring_sg" {
  name        = "monitoring_sg_${random_id.suffix.hex}"
  description = "Allow monitoring stack and SSH"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9090
    to_port     = 9090
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 9100
    to_port     = 9100
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_instance" "mini_vercel" {
  ami                         = "ami-0a1235697f4afa8a4" # Amazon Linux 2
  instance_type               = "t2.micro"
  key_name                    = var.key_name
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.monitoring_sg.id]

  tags = {
    Name = "MiniVercel"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo dnf update -y",
      "sudo dnf install -y docker",
      "sudo systemctl enable docker",
      "sudo systemctl start docker",
      "mkdir -p /home/ec2-user/prometheus",
      "echo 'global:\n  scrape_interval: 15s\nscrape_configs:\n  - job_name: \"cadvisor\"\n    static_configs:\n      - targets: [\"localhost:8080\"]' > /home/ec2-user/prometheus/prometheus.yml",
      "sudo docker run -d --name=prometheus -p 9090:9090 -v /home/ec2-user/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus",
      "sudo docker run -d --name=grafana -p 3000:3000 grafana/grafana-oss",
      "sudo docker run -d --name=cadvisor -p 8080:8080 -v /:/rootfs:ro -v /var/run:/var/run:rw -v /sys:/sys:ro -v /var/lib/docker/:/var/lib/docker:ro --device=/dev/kmsg gcr.io/cadvisor/cadvisor:latest",
      "sudo docker run -d --name node_exporter -p 9100:9100 --restart unless-stopped prom/node-exporter",
    ]

    connection { 
      type        = "ssh"
      user        = "ec2-user"
      private_key = file(var.private_key_path)
      host        = self.public_ip
    }
  }
}

