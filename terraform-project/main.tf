resource "aws_instance" "myweb" {
	ami=var.ami_id
	instance_type=var.instance_type
	key_name = "my_first_key"
	
	vpc_security_group_ids=  [aws_security_group.image_sg.id]
	iam_instance_profile = aws_iam_instance_profile.image_resizer_profile.name
}


resource "aws_security_group" "image_sg" {
	name="image-security-group"
	description="security group for image-resizer" 

	ingress {
		description = "allow http"
		from_port   = 80
		to_port     = 80
		protocol    = "tcp"
                cidr_blocks = ["0.0.0.0/0"]
	}
	ingress {
    		description = "Allow SSH"
    		from_port   = 22
    		to_port     = 22
    		protocol    = "tcp"
    		cidr_blocks = ["0.0.0.0/0"]
  	}
	egress {
    		description = "Allow all outbound traffic"
    		from_port   = 0
    		to_port     = 0
    		protocol    = "-1"
    		cidr_blocks = ["0.0.0.0/0"]
  	}
}

resource "aws_iam_role" "image_resizer_role" {
  name = "image-resizer-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "image_resizer_s3_policy" {

  name = "image-resizer-s3-policy"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]

        Resource = "arn:aws:s3:::image-resizer-nitin-2026/*"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "image_resizer_s3_attachment" {

  role       = aws_iam_role.image_resizer_role.name
  policy_arn = aws_iam_policy.image_resizer_s3_policy.arn
}

resource "aws_iam_instance_profile" "image_resizer_profile" {
  name = "image-resizer-ec2-profile"
  role = aws_iam_role.image_resizer_role.name
}











