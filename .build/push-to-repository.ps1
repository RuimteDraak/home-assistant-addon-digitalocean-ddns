git clone https://x-access-token:$(env:gitRepositoryToken)@github.com/$(env:repository)

$file = "$(Build.SourcesDirectory)/config.json"
$json = (Get-Content -Path $file | Out-String | ConvertFrom-Json)
Write-Host "$json"
$version = $json.version

if (!(Test-Path "$(Build.SourcesDirectory)/hassio-repository/hassio-$(env:addonName)" -PathType Container)) {
  New-Item -Path "$(Build.SourcesDirectory)/hassio-repository" -Name "hassio-$(env:addonName)" -ItemType "directory"
  Write-Host "Created new directory hassio-$(env:addonName)"
}

Set-Location hassio-repository/hassio-$(env:addonName)
if (Test-Path "config.json" -PathType Leaf) {
  $json = (Get-Content -Path "config.json" | Out-String | ConvertFrom-Json)
  $currentVersion = $json.version

  if ([version]$version -gt [version]$currentVersion) {
    Write-Host "New version bigger then previous version"
  }
  else {
    Write-Host "Current version already greater, not updating repository"
    Exit 0
  }
}
else {
  Write-Host "No config found, creating first registration"
}

Copy-Item -Path "$(Build.SourcesDirectory)/config.json" -Destination "$(Build.SourcesDirectory)/hassio-repository/hassio-$(env:addonName)/config.json"
Copy-Item -Path "$(Build.SourcesDirectory)/README.md" -Destination "$(Build.SourcesDirectory)/hassio-repository/hassio-$(env:addonName)/README.md"
Copy-Item -Path "$(Build.SourcesDirectory)/icon.png" -Destination "$(Build.SourcesDirectory)/hassio-repository/hassio-$(env:addonName)/icon.png"
Copy-Item -Path "$(Build.SourcesDirectory)/logo.png" -Destination "$(Build.SourcesDirectory)/hassio-repository/hassio-$(env:addonName)/logo.png"

git config --global user.email "RuimteDraak@no-reply.nl"
git config --global user.name "RuimteDraak"
git add --all
git commit -m "Update $(env:addonName) to version $version"
git push

Pop-Location
Write-Host "Updated repository to version $version"