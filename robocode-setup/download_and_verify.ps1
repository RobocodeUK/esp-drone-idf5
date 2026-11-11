# Downloads a file (resuming if partly downloaded) and checks its SHA-256.
# Exit code 0 = file is present and matches. Anything else = failed.
param(
    [Parameter(Mandatory = $true)][string]$Url,
    [Parameter(Mandatory = $true)][string]$Out,
    [Parameter(Mandatory = $true)][string]$Sha256
)
$ErrorActionPreference = 'Stop'

function Test-Hash($path) {
    (Test-Path $path) -and ((Get-FileHash $path -Algorithm SHA256).Hash -ieq $Sha256)
}

New-Item -ItemType Directory -Force (Split-Path $Out) | Out-Null

if (Test-Hash $Out) {
    Write-Host "      Already downloaded: $(Split-Path $Out -Leaf)"
    exit 0
}

Write-Host "      Downloading $(Split-Path $Out -Leaf) ..."
& curl.exe -L --fail --retry 3 -C - --progress-bar -o $Out $Url
if ($LASTEXITCODE -ne 0 -and -not (Test-Path $Out)) {
    Write-Host "      ERROR: download failed. Check the internet connection." -ForegroundColor Red
    exit 1
}

if (Test-Hash $Out) {
    Write-Host "      Download verified (SHA-256 OK)."
    exit 0
}

# A bad partial file can't be resumed; start again once from scratch.
Remove-Item $Out -Force -ErrorAction SilentlyContinue
Write-Host "      Retrying download from the start ..."
& curl.exe -L --fail --retry 3 --progress-bar -o $Out $Url
if (Test-Hash $Out) {
    Write-Host "      Download verified (SHA-256 OK)."
    exit 0
}
Remove-Item $Out -Force -ErrorAction SilentlyContinue
Write-Host "      ERROR: the downloaded file does not match the expected fingerprint (SHA-256)." -ForegroundColor Red
Write-Host "      It was deleted and not run. Try again later or ask your teacher." -ForegroundColor Red
exit 2
