output "instance_id" {
  value = aws_instance.mini_vercel.id
}

output "public_ip" {
  value = aws_instance.mini_vercel.public_ip
}