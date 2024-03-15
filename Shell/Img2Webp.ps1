function Img2Webp {
    Write-Host "------------------------------------------------------------"
    Write-Host "Gallery            : $PWD"
    # 获取全部图片
    $imageFiles = Get-ChildItem -Path . -Include *.png, *.jpg, *.jpeg, *.gif -File -Recurse -Hidden
    
    if ($imageFiles.Count -eq 0) {
        Write-Host "No images found." # 如果没有图片则跳过
        Write-Host "------------------------------------------------------------"
        continue
    }
    # 计算图片大小
    $totalSize = ($imageFiles | Measure-Object -Property Length -Sum).Sum
    Write-Host "Origin images size : $totalSize bytes"
    # 定义图片转码的代码块
    $convertScriptBlock = {
        param ($inputFile)
        ffmpeg -i $inputFile -c:v libwebp -q:v 100 "$($inputFile.BaseName).webp" -loglevel quiet -n
        Remove-Item -LiteralPath $inputFile.FullName -Force # 删除原始图片
    }
    # 启动代码块的任务
    $jobs = $imageFiles | ForEach-Object {
        Start-Job -ScriptBlock $convertScriptBlock -ArgumentList $_
    }
    $jobs | Wait-Job | Receive-Job # 等待任务完成
    $jobs | Remove-Job # 删除任务

    # 获取转码后的webp文件
    $webpFiles = Get-ChildItem -Path . -Include *.webp -File -Recurse -Hidden
    # 计算webp文件大小
    $webpTotalSize = ($webpFiles | Measure-Object -Property Length -Sum).Sum
    Write-Host "Convert images size: $totalWebpSize bytes"

    # 计算压缩率
    $compressionRate = [math]::Round(($webpTotalSize / $totalSize) * 100, 2)
    Write-Host "Compression rate   : $compressionRate%"
    Write-Host "------------------------------------------------------------"
}
function Img2Webp_subfolder {
    $galleries = Get-ChildItem -Path . -Directory -Hidden
    foreach ($gallery in $galleries) {
        Write-Host "------------------------------------------------------------"
        Write-Host "Gallery            : $($gallery.Name)"
        # 获取$gallary的全部图片
        $imageFiles = Get-ChildItem -LiteralPath $gallery.FullName -Include *.png, *.jpg, *.jpeg, *.gif -File -Recurse -Hidden
        
        if ($imageFiles.Count -eq 0) {
            Write-Host "No images found." # 如果没有图片则跳过
            Write-Host "------------------------------------------------------------"
            continue
        }
        # 计算图片大小
        $totalSize = ($imageFiles | Measure-Object -Property Length -Sum).Sum
        Write-Host "Origin images size : $totalSize bytes"
        # 定义图片转码的代码块
        $convertScriptBlock = {
            param ($inputFile)
            ffmpeg -i $inputFile -c:v libwebp -q:v 100 "$($inputFile.DirectoryName)/$($inputFile.BaseName).webp" -loglevel quiet -n
            Remove-Item -LiteralPath $inputFile.FullName -Force # 删除原始图片
        }
        # 启动代码块的任务
        $jobs = $imageFiles | ForEach-Object {
            Start-Job -ScriptBlock $convertScriptBlock -ArgumentList $_
        }
        $jobs | Wait-Job | Receive-Job  # 等待任务完成
        $jobs | Remove-Job # 删除任务
        
        # 获取转码后的webp文件
        $webpFiles = Get-ChildItem -LiteralPath $gallery.FullName -Include *.webp -File -Recurse -Hidden
        # 计算webp文件大小
        $totalWebpSize = ($webpFiles | Measure-Object -Property Length -Sum).Sum
        Write-Host "Convert images size: $totalWebpSize bytes"

        # 计算压缩率
        $compressionRate = [math]::Round(($totalWebpSize / $totalSize) * 100, 2)
        Write-Host "Compression rate   : $compressionRate%"
        Write-Host "------------------------------------------------------------"
    }
}