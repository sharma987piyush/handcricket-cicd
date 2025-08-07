pipeline{
    agent any
    environment{
        your-registry = ''
        your-image = 'cricket'
        ecr-url = ''
        registryCredential = ''
    }
    stages {
        stage(" building docker image "){
            steps{
                script{
                    def cricket = docker.build("your-registry/your-image:${env.BUILD_NUMBER}") 
                }
            }
        }
        stage(" login in aws ecr "){
            steps{
                script{
                    def docker.withRegistry( ecr-url , registryCredential )
                }
            }
        }
        stage(" pushing docker image to ecr ") {
            steps{
                script{
                    def dockerImage.push()
                }
            }
        }
        stage(" making pod from docker image "){
            steps{
                sh 'kubectl apply -f deploy.yml'
            }
        }
        stage(" applying service file for pod "){
            steps{
                sh 'kubectl apply -f service.yml'
            }
        }
    }
}