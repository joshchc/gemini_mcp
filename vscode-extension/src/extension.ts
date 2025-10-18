import * as vscode from 'vscode';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';

let mcpServerProcess: ChildProcess | null = null;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    console.log('Gemini MCP Copilot extension activated');
    
    outputChannel = vscode.window.createOutputChannel('Gemini MCP');
    
    // Register commands
    let startServerCommand = vscode.commands.registerCommand('gemini-mcp.startServer', startMCPServer);
    let stopServerCommand = vscode.commands.registerCommand('gemini-mcp.stopServer', stopMCPServer);
    let chatCommand = vscode.commands.registerCommand('gemini-mcp.chat', chatWithGemini);
    let generateCodeCommand = vscode.commands.registerCommand('gemini-mcp.generateCode', generateCode);
    let explainCodeCommand = vscode.commands.registerCommand('gemini-mcp.explainCode', explainCode);
    let refactorCodeCommand = vscode.commands.registerCommand('gemini-mcp.refactorCode', refactorCode);

    context.subscriptions.push(
        startServerCommand,
        stopServerCommand, 
        chatCommand,
        generateCodeCommand,
        explainCodeCommand,
        refactorCodeCommand,
        outputChannel
    );

    // Auto start server if configured
    const config = vscode.workspace.getConfiguration('gemini-mcp');
    if (config.get('autoStart')) {
        startMCPServer();
    }
}

async function startMCPServer() {
    if (mcpServerProcess) {
        vscode.window.showWarningMessage('MCP Server is already running');
        return;
    }

    const config = vscode.workspace.getConfiguration('gemini-mcp');
    const apiKey = config.get<string>('apiKey');
    const serverPath = config.get<string>('serverPath');

    if (!apiKey) {
        vscode.window.showErrorMessage('Please set your Gemini API key in settings');
        return;
    }

    if (!serverPath) {
        vscode.window.showErrorMessage('Please set the MCP server path in settings');
        return;
    }

    try {
        outputChannel.appendLine('Starting Gemini MCP Server...');
        
        mcpServerProcess = spawn('python', [serverPath], {
            env: {
                ...process.env,
                GEMINI_API_KEY: apiKey
            },
            cwd: path.dirname(serverPath)
        });

        mcpServerProcess.stdout?.on('data', (data) => {
            outputChannel.appendLine(`Server: ${data}`);
        });

        mcpServerProcess.stderr?.on('data', (data) => {
            outputChannel.appendLine(`Server Error: ${data}`);
        });

        mcpServerProcess.on('close', (code) => {
            outputChannel.appendLine(`Server exited with code ${code}`);
            mcpServerProcess = null;
        });

        vscode.window.showInformationMessage('Gemini MCP Server started successfully');
        
    } catch (error) {
        vscode.window.showErrorMessage(`Failed to start MCP server: ${error}`);
    }
}

async function stopMCPServer() {
    if (!mcpServerProcess) {
        vscode.window.showWarningMessage('MCP Server is not running');
        return;
    }

    mcpServerProcess.kill();
    mcpServerProcess = null;
    outputChannel.appendLine('MCP Server stopped');
    vscode.window.showInformationMessage('MCP Server stopped');
}

async function chatWithGemini() {
    const message = await vscode.window.showInputBox({
        prompt: 'Enter your message for Gemini',
        placeHolder: 'Type your question or request...'
    });

    if (!message) return;

    try {
        const response = await callMCPTool('chat', { message });
        showResponse('Gemini Chat', response);
    } catch (error) {
        vscode.window.showErrorMessage(`Chat failed: ${error}`);
    }
}

async function generateCode() {
    const description = await vscode.window.showInputBox({
        prompt: 'Describe the code you want to generate',
        placeHolder: 'e.g., A function to calculate fibonacci numbers'
    });

    if (!description) return;

    const language = await vscode.window.showQuickPick([
        'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'Go', 'Rust'
    ], {
        placeHolder: 'Select programming language'
    });

    if (!language) return;

    try {
        const response = await callMCPTool('generate_code', { 
            description, 
            language 
        });
        insertCodeIntoEditor(response);
    } catch (error) {
        vscode.window.showErrorMessage(`Code generation failed: ${error}`);
    }
}

async function explainCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.selection.isEmpty) {
        vscode.window.showWarningMessage('Please select some code to explain');
        return;
    }

    const selectedCode = editor.document.getText(editor.selection);

    try {
        const response = await callMCPTool('explain_code', { 
            code: selectedCode 
        });
        showResponse('Code Explanation', response);
    } catch (error) {
        vscode.window.showErrorMessage(`Code explanation failed: ${error}`);
    }
}

async function refactorCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.selection.isEmpty) {
        vscode.window.showWarningMessage('Please select some code to refactor');
        return;
    }

    const selectedCode = editor.document.getText(editor.selection);

    try {
        const response = await callMCPTool('refactor_code', { 
            code: selectedCode 
        });
        showResponse('Refactoring Suggestions', response);
    } catch (error) {
        vscode.window.showErrorMessage(`Code refactoring failed: ${error}`);
    }
}

async function callMCPTool(toolName: string, args: any): Promise<string> {
    // This is a simplified implementation
    // In a real implementation, you would communicate with the MCP server
    // through proper IPC or HTTP
    return new Promise((resolve, reject) => {
        // Simulate MCP tool call
        setTimeout(() => {
            resolve(`Mock response for ${toolName} with args: ${JSON.stringify(args)}`);
        }, 1000);
    });
}

function showResponse(title: string, content: string) {
    const panel = vscode.window.createWebviewPanel(
        'geminiResponse',
        title,
        vscode.ViewColumn.Beside,
        { enableScripts: true }
    );

    panel.webview.html = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>${title}</title>
            <style>
                body { 
                    font-family: var(--vscode-font-family);
                    padding: 20px;
                    line-height: 1.6;
                }
                pre {
                    background-color: var(--vscode-textBlockQuote-background);
                    padding: 10px;
                    border-radius: 4px;
                    overflow-x: auto;
                }
                code {
                    background-color: var(--vscode-textBlockQuote-background);
                    padding: 2px 4px;
                    border-radius: 2px;
                }
            </style>
        </head>
        <body>
            <h1>${title}</h1>
            <div>${content.replace(/\n/g, '<br>')}</div>
        </body>
        </html>
    `;
}

function insertCodeIntoEditor(code: string) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    editor.edit(editBuilder => {
        editBuilder.insert(editor.selection.active, code);
    });
}

export function deactivate() {
    if (mcpServerProcess) {
        mcpServerProcess.kill();
    }
}