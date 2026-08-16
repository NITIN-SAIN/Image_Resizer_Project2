output "public_ip" {
	description = "public IP address of the ec2 instance"
	value = aws_instance.myweb.public_ip
}

