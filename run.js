#!/usr/bin/env node

import { spawn } from 'cross-spawn';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Check if Python is installed
const checkPython = () => {
  const pythonCommands = ['python3', 'python'];
  
  for (const cmd of pythonCommands) {
    try {
      const result = spawn.sync(cmd, ['--version'], { stdio: 'pipe' });
      if (result.status === 0) {
        return cmd;
      }
    } catch (e) {
      continue;
    }
  }
  
  console.error('❌ Python is not installed. Please install Python 3.10 or higher.');
  console.error('   Visit: https://www.python.org/downloads/');
  process.exit(1);
};

// Check if dependencies are installed
const checkDependencies = (pythonCmd) => {
  const checkResult = spawn.sync(pythonCmd, ['-c', 'import fastmcp'], { 
    stdio: 'pipe',
    cwd: __dirname 
  });
  
  if (checkResult.status !== 0) {
    console.log('📦 Installing dependencies...');
    const installResult = spawn.sync(pythonCmd, ['-m', 'pip', 'install', '-e', '.'], {
      stdio: 'inherit',
      cwd: __dirname
    });
    
    if (installResult.status !== 0) {
      console.error('❌ Failed to install dependencies');
      process.exit(1);
    }
  }
};

// Check for .env file
const checkEnvFile = () => {
  const envPath = join(__dirname, '.env');
  const envExamplePath = join(__dirname, '.env.example');
  
  if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
    console.log('📝 Creating .env file from .env.example');
    console.log('   Please add your API keys to .env file');
    fs.copyFileSync(envExamplePath, envPath);
  }
};

// Main execution
const main = () => {
  console.log('🚀 Starting AI API MCP Server...\n');
  
  const pythonCmd = checkPython();
  checkDependencies(pythonCmd);
  checkEnvFile();
  
  // Start the server
  const server = spawn(pythonCmd, ['-m', 'src.server'], {
    stdio: 'inherit',
    cwd: __dirname,
    env: { ...process.env, PYTHONPATH: __dirname }
  });
  
  // Handle exit
  process.on('SIGINT', () => {
    server.kill('SIGINT');
    process.exit(0);
  });
  
  server.on('error', (err) => {
    console.error('❌ Failed to start server:', err);
    process.exit(1);
  });
  
  server.on('exit', (code) => {
    process.exit(code || 0);
  });
};

main();