#!/usr/bin/env node

const http = require('http');
const os = require('os');

console.log('🌐 坦克大战游戏 - 网络诊断工具\n');

// 获取网络接口信息
function getNetworkInfo() {
    const interfaces = os.networkInterfaces();
    const validInterfaces = [];
    
    Object.keys(interfaces).forEach(name => {
        interfaces[name].forEach(interface => {
            // 只显示IPv4地址，排除回环地址
            if (interface.family === 'IPv4' && !interface.internal) {
                validInterfaces.push({
                    name: name,
                    address: interface.address,
                    netmask: interface.netmask
                });
            }
        });
    });
    
    return validInterfaces;
}

// 测试端口是否可访问
function testPort(host, port) {
    return new Promise((resolve) => {
        const req = http.request({
            host: host,
            port: port,
            path: '/',
            method: 'GET',
            timeout: 3000
        }, (res) => {
            resolve({ success: true, status: res.statusCode });
        });
        
        req.on('error', () => {
            resolve({ success: false });
        });
        
        req.on('timeout', () => {
            req.destroy();
            resolve({ success: false });
        });
        
        req.end();
    });
}

async function main() {
    console.log('📊 网络接口信息:');
    const interfaces = getNetworkInfo();
    
    if (interfaces.length === 0) {
        console.log('❌ 未找到有效的网络接口');
        return;
    }
    
    interfaces.forEach((iface, index) => {
        console.log(`${index + 1}. ${iface.name}: ${iface.address}`);
    });
    
    console.log('\n🔍 测试游戏服务器连接...');
    
    // 测试本地连接
    const localTest = await testPort('localhost', 8080);
    if (localTest.success) {
        console.log('✅ 本地服务器运行正常 (localhost:8080)');
    } else {
        console.log('❌ 本地服务器连接失败');
    }
    
    // 测试所有网络接口
    for (const iface of interfaces) {
        const test = await testPort(iface.address, 8080);
        if (test.success) {
            console.log(`✅ 网络接口 ${iface.name} 可访问: http://${iface.address}:8080`);
        } else {
            console.log(`❌ 网络接口 ${iface.name} 不可访问: ${iface.address}:8080`);
        }
    }
    
    console.log('\n📱 移动设备连接指南:');
    console.log('1. 确保移动设备和电脑在同一WiFi网络');
    console.log('2. 在移动设备浏览器中输入以下地址之一:');
    
    interfaces.forEach(iface => {
        console.log(`   - http://${iface.address}:8080`);
    });
    
    console.log('\n🎮 游戏控制:');
    console.log('- 移动端: 屏幕底部的虚拟方向键和射击按钮');
    console.log('- 桌面端: WASD移动，空格射击，R重新开始');
    
    console.log('\n🔧 故障排除:');
    console.log('- 如果无法连接，检查防火墙设置');
    console.log('- 确保端口8080未被其他程序占用');
    console.log('- 尝试使用其他端口（3000、8000等）');
    console.log('- 检查路由器设置是否阻止了端口访问');
    
    console.log('\n💡 提示:');
    console.log('- 建议使用Chrome或Firefox浏览器');
    console.log('- 游戏支持PWA，可以添加到主屏幕');
    console.log('- 横屏模式提供更好的游戏体验');
}

main().catch(console.error);