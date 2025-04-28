const { spawn } = require('child_process');
const path = require('path');

// 获取命令行参数
const args = process.argv.slice(2);

// 构建Python命令参数
const pythonArgs = ['main.py'];

// 处理日期参数
const dateIndex = args.indexOf('--date');
if (dateIndex !== -1 && args[dateIndex + 1]) {
    pythonArgs.push('--date', args[dateIndex + 1]);
}

// 处理类型参数
const typeIndex = args.indexOf('--type');
if (typeIndex !== -1 && args[typeIndex + 1]) {
    pythonArgs.push('--type', args[typeIndex + 1]);
}

// 执行Python脚本
const pythonProcess = spawn('python', pythonArgs, {
    stdio: 'inherit',
    shell: true
});

// 错误处理
pythonProcess.on('error', (err) => {
    console.error('启动Python程序时发生错误:', err);
    process.exit(1);
});

pythonProcess.on('close', (code) => {
    if (code !== 0) {
        console.error(`Python程序异常退出，退出码: ${code}`);
        process.exit(code);
    }
}); 