# MSA Infra #

### Overview ###

This repository is used to mantain the Terraform code, files and folders to implement Infra as Code on MyStoneridge microservices. 
We are using a module structure to work with Terraform when each microservice can implement its required group of resources. For example, some of microservices need the module Kinesis and some do not have this requirement. So to manage this, we have created a tf file for each microservice {app_name}.tf, and using this file, we have configured all the modules needed to implement it. 



### Getting Started ###

To get started with MSA Terraform project, you will need the following

* an AWS account with sufficient permissions to create and manage AWS resources
* Terraform installed on your local machine. You can use the official documentation to install it with the following link >  [Official Terraform Documentation](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
* The AWS CLI installed on your local machine [Official AWS Documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
* Git installed on your machine

To set up the environment, you can do it following these steps: 

1. Clone this repository to your local machine using git. 
2. Navigate to the terraform directory in the cloned repository.
3. Run the following command to initialize the Terraform project: 

```terraform init```


## How modules works:
In this section, we can see a brief of each module created in this project and what kind of task they will do. 

## certificates
The module manages AWS Certificate Manager (ACM) resouces. It is used as a requirement of Route53 zone 

## ecs
This module manages Elastic Container Service (ECS). All microservices running on MyStoneridge project were deployed used this service. 

## ecs_cluster
This module is a required resource of ECS. It creates a cluster to orchestrate the ECS containers. 

## load_balancer
This module manages Load Balancer resouces. In our case, this module creates an Application Load Balancer and a Network Load Balancer. The traffic comming from the internet, uses first the NLB and it sends the traffic to the ALB and afterward send the packets to ECS.  

## network
This module handles the VPC and subnets that were created by IT Team, this module does not create the VPC and subnet, but only manages the resource IDs to provide it to the other resources. 

## policy
This module manages the IAM policies to assign it in resources when it is required. IAM policies use JSON language to enable and disable resource access. 

## resource_group
This module manages AWS Resource Groups. AWS Resource Groups makes it easier to manage and automate tasks on large numbers of AWS resources at one time.

## route53
Route53 module is used to configure Domain zone on AWS, in this case, creates a zone and a DNS record.  

## security_group
This module is used to configure the ALB security group rules.

## target_group
This module manages Target Group resources for the load balancer. Each target group is used to route requests to one or more registered targets. It handles the ALB and NLB target groups and its respective listeners.

### Recommended Architecture ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

## GitLab Pipeline Configuration

The pipeline configuration defines which steps are run for each branch:

- `develop` branch: runs the Validate, Plan, and Dev Deploy steps, applying it on DEV account.
- `staging` branch: runs the Validate, Plan, and Staging Deploy steps, applying it on QA account.
- `master` branch: runs the Validate, Plan, and Prod Deploy steps, applying it on PROD account.

## How to Contribute:

1. Fork this repository on GitHub to create a copy of the project in your own account.
2. Clone the forked repository to your local machine using Git.
3. Create a new branch for your changes:

```
   git checkout -b my-feature-branch
```
4. Make the necessary changes to the Terraform code and commit the changes to your branch:

```
   git add .
   git commit -m "#TICKET-NUMBER# Add new feature"
```

5. Push the changes to your forked repository:

```
   git push origin my-feature-branch
```

6. Create a pull request (PR) on the original repository to propose your changes. Make sure to include a detailed description of the changes and the reasoning behind them.

We will review your PR and provide feedback as necessary. Once the changes have been approved, we will merge the PR into the main branch of the repository.

When contributing to the project, please follow the existing coding standards and best practices. Additionally, please ensure that your changes do not introduce any security vulnerabilities or other issues. It is also recommended to test your changes locally before submitting a PR.

Thank you for your contributions to the MyStoneridge Terraform project!
