pipeline {
    agent any

    environment {
        IMAGE_NAME = "nitinsain012/image-resizer-app"
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {

        stage('Clone repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/NITIN-SAIN/Image_Resizer_Project2.git'
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    )
                ]) {

                    sh '''
                        echo $PASSWORD | docker login -u $USERNAME --password-stdin
                        docker push $IMAGE_NAME:$IMAGE_TAG
                        docker logout
                    '''
                }
            }
        }

        stage('Launch EC2 using Terraform') {
            steps {
                dir('terraform-project') {

                    sh 'terraform init'

                    sh 'terraform plan'

                    sh 'terraform apply -auto-approve'
                }
            }
        }
        
        stage('Deploy with Ansible') {
            steps {
                sshagent(['aws-ec2-ssh']) {
                    sh '''
                        cd terraform-project

                        EC2_IP=$(terraform output -raw public_ip)

                        ansible-playbook \
                        -i "$EC2_IP," \
                        -u ubuntu \
                        ../ansible/playbook.yml \
			-e "docker_tag=${IMAGE_TAG}"
                    '''
                }
            }
        }
    }
}
