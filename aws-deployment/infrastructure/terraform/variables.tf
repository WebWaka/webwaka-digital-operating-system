# WebWaka Digital Operating System - Terraform Variables

# Project Configuration
variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "webwaka"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "production"
  
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

# AWS Configuration
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

# Domain Configuration
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "webwaka.com"
}

variable "create_route53_zone" {
  description = "Whether to create Route 53 hosted zone"
  type        = bool
  default     = false
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24", "10.0.30.0/24"]
}

variable "database_subnet_cidrs" {
  description = "CIDR blocks for database subnets"
  type        = list(string)
  default     = ["10.0.100.0/24", "10.0.200.0/24", "10.0.300.0/24"]
}

# EC2 Configuration
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "min_size" {
  description = "Minimum number of instances in ASG"
  type        = number
  default     = 2
}

variable "max_size" {
  description = "Maximum number of instances in ASG"
  type        = number
  default     = 10
}

variable "desired_capacity" {
  description = "Desired number of instances in ASG"
  type        = number
  default     = 3
}

variable "key_pair_name" {
  description = "Name of the EC2 Key Pair"
  type        = string
  default     = "webwaka-keypair"
}

# Database Configuration
variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "webwaka"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "webwaka_admin"
}

variable "db_allocated_storage" {
  description = "Database allocated storage in GB"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "Database maximum allocated storage in GB"
  type        = number
  default     = 100
}

variable "db_backup_retention_period" {
  description = "Database backup retention period in days"
  type        = number
  default     = 7
}

variable "db_multi_az" {
  description = "Enable Multi-AZ deployment for RDS"
  type        = bool
  default     = true
}

# ElastiCache Configuration
variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.t3.micro"
}

variable "redis_num_cache_nodes" {
  description = "Number of cache nodes"
  type        = number
  default     = 1
}

variable "redis_port" {
  description = "Redis port"
  type        = number
  default     = 6379
}

# Load Balancer Configuration
variable "enable_deletion_protection" {
  description = "Enable deletion protection for load balancer"
  type        = bool
  default     = true
}

variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/api/health"
}

variable "health_check_interval" {
  description = "Health check interval in seconds"
  type        = number
  default     = 30
}

variable "health_check_timeout" {
  description = "Health check timeout in seconds"
  type        = number
  default     = 5
}

variable "healthy_threshold" {
  description = "Number of consecutive health checks successes required"
  type        = number
  default     = 2
}

variable "unhealthy_threshold" {
  description = "Number of consecutive health check failures required"
  type        = number
  default     = 3
}

# CloudFront Configuration
variable "cloudfront_price_class" {
  description = "CloudFront price class"
  type        = string
  default     = "PriceClass_All"
  
  validation {
    condition     = contains(["PriceClass_100", "PriceClass_200", "PriceClass_All"], var.cloudfront_price_class)
    error_message = "CloudFront price class must be PriceClass_100, PriceClass_200, or PriceClass_All."
  }
}

variable "cloudfront_minimum_protocol_version" {
  description = "Minimum SSL protocol version for CloudFront"
  type        = string
  default     = "TLSv1.2_2021"
}

# Monitoring Configuration
variable "enable_detailed_monitoring" {
  description = "Enable detailed monitoring for EC2 instances"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

# Security Configuration
variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the application"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "enable_waf" {
  description = "Enable AWS WAF"
  type        = bool
  default     = true
}

variable "enable_shield" {
  description = "Enable AWS Shield Advanced"
  type        = bool
  default     = false
}

# Backup Configuration
variable "backup_schedule" {
  description = "Backup schedule expression"
  type        = string
  default     = "cron(0 2 * * ? *)"  # Daily at 2 AM UTC
}

variable "backup_retention_days" {
  description = "Backup retention period in days"
  type        = number
  default     = 30
}

# Ubuntu Philosophy Configuration
variable "ubuntu_principles" {
  description = "Ubuntu philosophy principles for tagging and configuration"
  type = object({
    community_centered      = string
    traditional_leadership = string
    fair_sharing           = string
    cultural_sensitivity   = string
  })
  default = {
    community_centered      = "I am because we are"
    traditional_leadership = "Respect for elders and wisdom"
    fair_sharing           = "Ubuntu fair distribution"
    cultural_sensitivity   = "African values first"
  }
}

# African Market Optimization
variable "african_optimization" {
  description = "African market optimization settings"
  type = object({
    mobile_first     = bool
    low_bandwidth    = bool
    multi_currency   = bool
    offline_support  = bool
    edge_locations   = list(string)
  })
  default = {
    mobile_first     = true
    low_bandwidth    = true
    multi_currency   = true
    offline_support  = true
    edge_locations   = ["Cape Town", "Johannesburg", "Lagos", "Nairobi"]
  }
}

# Application Configuration
variable "app_config" {
  description = "Application configuration settings"
  type = object({
    debug_mode           = bool
    max_upload_size      = string
    session_timeout      = number
    rate_limit_requests  = number
    rate_limit_window    = number
  })
  default = {
    debug_mode           = false
    max_upload_size      = "10MB"
    session_timeout      = 3600
    rate_limit_requests  = 1000
    rate_limit_window    = 3600
  }
}

# Feature Flags
variable "feature_flags" {
  description = "Feature flags for enabling/disabling features"
  type = object({
    white_label_platform    = bool
    multi_level_referral   = bool
    payment_systems        = bool
    voice_interface        = bool
    mobile_optimization    = bool
    performance_monitoring = bool
    documentation_systems  = bool
    quality_assurance      = bool
  })
  default = {
    white_label_platform    = true
    multi_level_referral   = true
    payment_systems        = true
    voice_interface        = true
    mobile_optimization    = true
    performance_monitoring = true
    documentation_systems  = true
    quality_assurance      = true
  }
}

# Cost Optimization
variable "cost_optimization" {
  description = "Cost optimization settings"
  type = object({
    use_spot_instances     = bool
    enable_auto_scaling    = bool
    schedule_scaling       = bool
    reserved_instances     = bool
    lifecycle_policies     = bool
  })
  default = {
    use_spot_instances     = false
    enable_auto_scaling    = true
    schedule_scaling       = true
    reserved_instances     = true
    lifecycle_policies     = true
  }
}

# Disaster Recovery
variable "disaster_recovery" {
  description = "Disaster recovery configuration"
  type = object({
    enable_cross_region_backup = bool
    backup_regions            = list(string)
    rto_minutes              = number
    rpo_minutes              = number
  })
  default = {
    enable_cross_region_backup = true
    backup_regions            = ["us-west-2", "eu-west-1"]
    rto_minutes              = 60
    rpo_minutes              = 15
  }
}

# Compliance and Security
variable "compliance" {
  description = "Compliance and security settings"
  type = object({
    enable_encryption_at_rest   = bool
    enable_encryption_in_transit = bool
    enable_audit_logging       = bool
    enable_access_logging      = bool
    data_residency_region      = string
  })
  default = {
    enable_encryption_at_rest   = true
    enable_encryption_in_transit = true
    enable_audit_logging       = true
    enable_access_logging      = true
    data_residency_region      = "us-east-1"
  }
}

# Performance Configuration
variable "performance" {
  description = "Performance optimization settings"
  type = object({
    enable_caching           = bool
    cache_ttl_seconds       = number
    enable_compression      = bool
    enable_http2            = bool
    connection_timeout      = number
    request_timeout         = number
  })
  default = {
    enable_caching           = true
    cache_ttl_seconds       = 3600
    enable_compression      = true
    enable_http2            = true
    connection_timeout      = 30
    request_timeout         = 300
  }
}

# Notification Configuration
variable "notifications" {
  description = "Notification settings"
  type = object({
    email_alerts           = list(string)
    slack_webhook_url      = string
    sms_alerts            = list(string)
    enable_critical_alerts = bool
    enable_warning_alerts  = bool
  })
  default = {
    email_alerts           = []
    slack_webhook_url      = ""
    sms_alerts            = []
    enable_critical_alerts = true
    enable_warning_alerts  = true
  }
}

# Development Configuration
variable "development" {
  description = "Development and testing configuration"
  type = object({
    enable_debug_endpoints = bool
    enable_test_data      = bool
    enable_profiling      = bool
    log_level            = string
  })
  default = {
    enable_debug_endpoints = false
    enable_test_data      = false
    enable_profiling      = false
    log_level            = "INFO"
  }
}

