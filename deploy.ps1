# 检查Python环境
Write-Host "检查Python环境..."
$pythonVersion = python --version
if (-not $?) {
    Write-Host "错误: 未找到Python，请先安装Python 3.7或更高版本"
    exit 1
}
Write-Host "Python版本: $pythonVersion"

# 检查Node.js环境
Write-Host "检查Node.js环境..."
$nodeVersion = node --version
if (-not $?) {
    Write-Host "错误: 未找到Node.js，请先安装Node.js 14.0或更高版本"
    exit 1
}
Write-Host "Node.js版本: $nodeVersion"

# 创建MCP目录
$mcpDir = "$env:USERPROFILE\.cursor\mcp"
if (-not (Test-Path $mcpDir)) {
    Write-Host "创建MCP目录: $mcpDir"
    New-Item -ItemType Directory -Path $mcpDir -Force
}

# 复制文件到MCP目录
Write-Host "复制文件到MCP目录..."
Copy-Item -Path "main.py" -Destination "$mcpDir\main.py" -Force
Copy-Item -Path "index.js" -Destination "$mcpDir\index.js" -Force
Copy-Item -Path "mcp.json" -Destination "$mcpDir\mcp.json" -Force
Copy-Item -Path "package.json" -Destination "$mcpDir\package.json" -Force

# 安装Python依赖
Write-Host "安装Python依赖..."
pip install akshare==1.11.22 pandas==2.0.3

Write-Host "`n部署完成！"
Write-Host "现在您可以使用以下命令获取涨停股票信息："
Write-Host "mcp zt [--date YYYYMMDD] [--type all|simple|stats]" 