# PowerShell script to create Lambda ZIP files
# Run this from the terraform directory

$lambdaDir = "lambda"
$pythonFiles = @(
    "generate_upload_url.py",
    "suggest_title.py", 
    "summarize.py",
    "rename_file.py",
    "metadata_handler.py",
    "list_files.py",
    "get_download_url.py",
    "delete_files.py",
    "stats.py"
)

foreach ($file in $pythonFiles) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file)
    $zipName = "$baseName.zip"
    
    Write-Host "Creating $zipName from $file..."
    
    # Remove existing ZIP if it exists
    if (Test-Path "$lambdaDir\$zipName") {
        Remove-Item "$lambdaDir\$zipName" -Force
    }
    
    # Create ZIP file
    Compress-Archive -Path "$lambdaDir\$file" -DestinationPath "$lambdaDir\$zipName"
}

Write-Host "All Lambda ZIP files created successfully!" 