/**
 * 印刷流程数字化系统 - 调试控制台
 * 这个脚本提供了一些调试功能，帮助诊断前端问题
 */

(function() {
    // 创建调试控制台
    function createDebugConsole() {
        // 检查是否已经存在调试控制台
        if (document.getElementById('debug-console')) {
            return;
        }
        
        // 创建控制台元素
        const consoleContainer = document.createElement('div');
        consoleContainer.id = 'debug-console';
        consoleContainer.style.cssText = `
            position: fixed;
            bottom: 0;
            right: 0;
            width: 400px;
            height: 300px;
            background-color: rgba(0, 0, 0, 0.8);
            color: #00ff00;
            font-family: monospace;
            font-size: 12px;
            padding: 10px;
            overflow-y: auto;
            z-index: 9999;
            border-top-left-radius: 8px;
            display: none;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        `;
        
        // 创建控制台头部
        const consoleHeader = document.createElement('div');
        consoleHeader.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid #444;
        `;
        
        const consoleTitle = document.createElement('div');
        consoleTitle.textContent = '调试控制台';
        consoleTitle.style.fontWeight = 'bold';
        
        const closeButton = document.createElement('button');
        closeButton.textContent = 'X';
        closeButton.style.cssText = `
            background: none;
            border: none;
            color: #ff5555;
            cursor: pointer;
            font-weight: bold;
        `;
        closeButton.onclick = function() {
            consoleContainer.style.display = 'none';
        };
        
        consoleHeader.appendChild(consoleTitle);
        consoleHeader.appendChild(closeButton);
        consoleContainer.appendChild(consoleHeader);
        
        // 创建日志区域
        const logArea = document.createElement('div');
        logArea.id = 'debug-log';
        logArea.style.cssText = `
            height: 220px;
            overflow-y: auto;
            margin-bottom: 10px;
            padding: 5px;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 4px;
        `;
        consoleContainer.appendChild(logArea);
        
        // 创建控制按钮
        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = `
            display: flex;
            justify-content: space-between;
        `;
        
        const clearButton = document.createElement('button');
        clearButton.textContent = '清除日志';
        clearButton.style.cssText = `
            background-color: #333;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
        `;
        clearButton.onclick = function() {
            document.getElementById('debug-log').innerHTML = '';
        };
        
        const testApiButton = document.createElement('button');
        testApiButton.textContent = '测试API连接';
        testApiButton.style.cssText = `
            background-color: #2196f3;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 5px;
        `;
        testApiButton.onclick = testApiConnections;
        
        const reloadDataButton = document.createElement('button');
        reloadDataButton.textContent = '重新加载数据';
        reloadDataButton.style.cssText = `
            background-color: #4caf50;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            margin-left: 5px;
        `;
        reloadDataButton.onclick = function() {
            window.fetchData();
            log('正在重新加载数据...');
        };
        
        buttonContainer.appendChild(clearButton);
        buttonContainer.appendChild(testApiButton);
        buttonContainer.appendChild(reloadDataButton);
        consoleContainer.appendChild(buttonContainer);
        
        // 添加到页面
        document.body.appendChild(consoleContainer);
        
        // 添加快捷键
        document.addEventListener('keydown', function(e) {
            // Ctrl+Shift+D 显示/隐藏调试控制台
            if (e.ctrlKey && e.shiftKey && e.key === 'D') {
                e.preventDefault();
                consoleContainer.style.display = consoleContainer.style.display === 'none' ? 'block' : 'none';
            }
        });
        
        log('调试控制台已初始化，按 Ctrl+Shift+D 显示/隐藏');
    }
    
    // 添加日志
    function log(message, type = 'info') {
        const logArea = document.getElementById('debug-log');
        if (!logArea) return;
        
        const logItem = document.createElement('div');
        const timestamp = new Date().toLocaleTimeString();
        
        let color = '#00ff00'; // 默认绿色
        if (type === 'error') color = '#ff5555';
        if (type === 'warning') color = '#ffff55';
        
        logItem.style.cssText = `
            margin-bottom: 5px;
            color: ${color};
        `;
        
        logItem.innerHTML = `<span style="color: #aaaaaa;">[${timestamp}]</span> ${message}`;
        logArea.appendChild(logItem);
        logArea.scrollTop = logArea.scrollHeight;
    }
    
    // 测试API连接
    async function testApiConnections() {
        log('正在测试API连接...');
        
        const baseUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
            ? 'http://localhost:5000' 
            : '';
        
        // 测试健康检查API
        try {
            const healthResponse = await fetch(`${baseUrl}/health`);
            if (healthResponse.ok) {
                const healthData = await healthResponse.text();
                log(`健康检查API正常: ${healthData}`);
            } else {
                log(`健康检查API错误: ${healthResponse.status} ${healthResponse.statusText}`, 'error');
            }
        } catch (error) {
            log(`健康检查API异常: ${error.message}`, 'error');
        }
        
        // 测试订单API
        try {
            const ordersResponse = await fetch(`${baseUrl}/api/optimized_orders`);
            if (ordersResponse.ok) {
                const ordersData = await ordersResponse.json();
                log(`订单API正常: 获取到 ${ordersData.length} 条订单`);
                
                // 检查订单数据格式
                if (ordersData.length > 0) {
                    const firstOrder = ordersData[0];
                    log(`订单数据示例: ${JSON.stringify(firstOrder).substring(0, 100)}...`);
                    
                    // 检查必要字段
                    const requiredFields = ['order_id', 'product_name', 'printing_method', 'delivery_date'];
                    const missingFields = requiredFields.filter(field => !firstOrder.hasOwnProperty(field));
                    
                    if (missingFields.length > 0) {
                        log(`订单数据缺少字段: ${missingFields.join(', ')}`, 'warning');
                    } else {
                        log('订单数据格式正确');
                    }
                }
            } else {
                log(`订单API错误: ${ordersResponse.status} ${ordersResponse.statusText}`, 'error');
            }
        } catch (error) {
            log(`订单API异常: ${error.message}`, 'error');
        }
        
        // 测试指标API
        try {
            const metricsResponse = await fetch(`${baseUrl}/api/metrics`);
            if (metricsResponse.ok) {
                const metricsData = await metricsResponse.json();
                log(`指标API正常: ${JSON.stringify(metricsData)}`);
            } else {
                log(`指标API错误: ${metricsResponse.status} ${metricsResponse.statusText}`, 'error');
            }
        } catch (error) {
            log(`指标API异常: ${error.message}`, 'error');
        }
        
        // 测试设备API
        try {
            const devicesResponse = await fetch(`${baseUrl}/api/devices`);
            if (devicesResponse.ok) {
                const devicesData = await devicesResponse.json();
                log(`设备API正常: 获取到 ${devicesData.length} 条设备数据`);
            } else {
                log(`设备API错误: ${devicesResponse.status} ${devicesResponse.statusText}`, 'error');
            }
        } catch (error) {
            log(`设备API异常: ${error.message}`, 'error');
        }
    }
    
    // 拦截控制台日志
    const originalConsoleLog = console.log;
    const originalConsoleError = console.error;
    const originalConsoleWarn = console.warn;
    
    console.log = function() {
        originalConsoleLog.apply(console, arguments);
        log(Array.from(arguments).join(' '));
    };
    
    console.error = function() {
        originalConsoleError.apply(console, arguments);
        log(Array.from(arguments).join(' '), 'error');
    };
    
    console.warn = function() {
        originalConsoleWarn.apply(console, arguments);
        log(Array.from(arguments).join(' '), 'warning');
    };
    
    // 拦截未捕获的错误
    window.addEventListener('error', function(event) {
        log(`未捕获错误: ${event.message} at ${event.filename}:${event.lineno}:${event.colno}`, 'error');
    });
    
    // 拦截未处理的Promise拒绝
    window.addEventListener('unhandledrejection', function(event) {
        log(`未处理的Promise拒绝: ${event.reason}`, 'error');
    });
    
    // 页面加载完成后初始化调试控制台
    window.addEventListener('load', createDebugConsole);
    
    // 导出调试功能到全局
    window.debugConsole = {
        log,
        testApiConnections,
        show: function() {
            const console = document.getElementById('debug-console');
            if (console) {
                console.style.display = 'block';
            }
        },
        hide: function() {
            const console = document.getElementById('debug-console');
            if (console) {
                console.style.display = 'none';
            }
        }
    };
})(); 