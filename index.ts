export {};

const args = Deno.args;
const pythonArgs = ["main.py"];

// 处理 --date 参数
const dateIndex = args.indexOf("--date");
if (dateIndex !== -1 && args[dateIndex + 1]) {
  pythonArgs.push("--date", args[dateIndex + 1]);
}

// 处理 --type 参数
const typeIndex = args.indexOf("--type");
if (typeIndex !== -1 && args[typeIndex + 1]) {
  pythonArgs.push("--type", args[typeIndex + 1]);
}

// 调用 Python 脚本
const pyProcess = Deno.run({
  cmd: ["python", ...pythonArgs],
  stdout: "inherit",
  stderr: "inherit"
});

const pyStatus = await pyProcess.status();
if (!pyStatus.success) {
  console.error(`Python程序异常退出，退出码: ${pyStatus.code}`);
  Deno.exit(pyStatus.code);
} 