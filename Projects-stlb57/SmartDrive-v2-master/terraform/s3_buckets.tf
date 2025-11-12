resource "aws_s3_bucket" "upload_bucket" {
    bucket = "smartdrive-v2-upload-1234"
}

resource "aws_s3_bucket" "organized_bucket" {
    bucket = "smartdrive-v2-organized-1234"
}

# Block public access for upload bucket
resource "aws_s3_bucket_public_access_block" "upload_bucket_public_access_block" {
  bucket = aws_s3_bucket.upload_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Block public access for organized bucket
resource "aws_s3_bucket_public_access_block" "organized_bucket_public_access_block" {
  bucket = aws_s3_bucket.organized_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning for both buckets
resource "aws_s3_bucket_versioning" "upload_bucket_versioning" {
  bucket = aws_s3_bucket.upload_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "organized_bucket_versioning" {
  bucket = aws_s3_bucket.organized_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_cors_configuration" "upload_cors" {
  bucket = aws_s3_bucket.upload_bucket.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST", "GET"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}