#!/usr/bin/env node

/**
 * Build Sphinx documentation with nested submodule support
 *
 * This script:
 * 1. Checks for cleanroom-technical-docs submodule
 * 2. Verifies Python and Sphinx installation
 * 3. Builds documentation for all projects (subprojects + master) via Makefile
 * 4. Copies output to public/docs
 *
 * Uses `make html` which builds all subprojects first, then master docs,
 * ensuring consistent theming via the sphinx-theme submodule.
 */

import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

// Parse command line arguments
const args = process.argv.slice(2);
const shouldClean = args.includes('--clean');

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');
const technicalDocsDir = join(rootDir, 'cleanroom-technical-docs');
const outputDir = join(rootDir, 'public', 'docs');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
};

function log(message, color = colors.reset) {
  console.log(`${color}${message}${colors.reset}`);
}

function exec(command, cwd = rootDir, silent = false) {
  try {
    const output = execSync(command, { 
      cwd, 
      encoding: 'utf-8',
      stdio: silent ? 'pipe' : 'inherit'
    });
    return { success: true, output };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

function checkSubmodule() {
  log('\n📁 Checking for technical-docs submodule...', colors.blue);
  
  if (!existsSync(technicalDocsDir)) {
    log('❌ cleanroom-technical-docs submodule not found', colors.red);
    log('   Run: git submodule update --init --recursive', colors.yellow);
    return false;
  }
  
  if (!existsSync(join(technicalDocsDir, 'source'))) {
    log('❌ cleanroom-technical-docs appears incomplete', colors.red);
    log('   Run: git submodule update --init --recursive', colors.yellow);
    return false;
  }
  
  log('✓ Technical docs submodule found', colors.green);
  return true;
}

function checkPython() {
  log('\n🐍 Checking Python installation...', colors.blue);
  
  const result = exec('python3 --version', rootDir, true);
  if (!result.success) {
    log('❌ Python 3 not found', colors.red);
    log('   Install Python: https://www.python.org/downloads/', colors.yellow);
    return false;
  }
  
  log(`✓ ${result.output.trim()}`, colors.green);
  return true;
}

function setupVirtualEnv() {
  log('\n🔧 Setting up Python virtual environment...', colors.blue);
  
  const venvDir = join(technicalDocsDir, '.venv');
  
  if (!existsSync(venvDir)) {
    log('Creating virtual environment...', colors.blue);
    const result = exec('python3 -m venv .venv', technicalDocsDir);
    if (!result.success) {
      log('❌ Failed to create virtual environment', colors.red);
      return false;
    }
  }
  
  log('✓ Virtual environment ready', colors.green);
  return true;
}

function installDependencies() {
  log('\n📦 Installing Sphinx dependencies...', colors.blue);
  
  const activateCmd = process.platform === 'win32' 
    ? '.venv\\Scripts\\activate' 
    : 'source .venv/bin/activate';
  
  const pipCmd = process.platform === 'win32'
    ? '.venv\\Scripts\\pip'
    : '.venv/bin/pip';
  
  const result = exec(
    `${pipCmd} install -q -r requirements.txt`,
    technicalDocsDir
  );
  
  if (!result.success) {
    log('❌ Failed to install dependencies', colors.red);
    return false;
  }
  
  log('✓ Dependencies installed', colors.green);
  return true;
}

function cleanBuild() {
  log('\n🧹 Cleaning previous build...', colors.blue);
  const result = exec('make clean', technicalDocsDir);
  if (!result.success) {
    log('⚠️  Clean failed, continuing anyway...', colors.yellow);
  } else {
    log('✓ Build cleaned', colors.green);
  }
  return true; // Don't fail the build if clean fails
}

function buildDocs() {
  log('\n📚 Building Sphinx documentation...', colors.blue);
  log('   Building all subprojects and master docs...', colors.blue);

  // Use the Makefile's html target which:
  // 1. Builds all subprojects (airgap-whisper-docs, airgap-deploy-docs, airgap-transfer-docs)
  // 2. Builds the master documentation
  // 3. Copies subproject builds into master build/html/
  // This ensures consistent theming across all docs

  // Use absolute path so it works when Makefile cds into subdirectories
  const sphinxBuild = process.platform === 'win32'
    ? join(technicalDocsDir, '.venv', 'Scripts', 'sphinx-build')
    : join(technicalDocsDir, '.venv', 'bin', 'sphinx-build');

  const result = exec(
    `make html SPHINXBUILD="${sphinxBuild}"`,
    technicalDocsDir
  );

  if (!result.success) {
    log('❌ Sphinx build failed', colors.red);
    return false;
  }

  log('✓ Documentation built successfully', colors.green);
  return true;
}

function copyOutput() {
  log('\n📋 Copying output to public/docs...', colors.blue);
  
  const sourceDir = join(technicalDocsDir, 'build', 'html');
  
  if (!existsSync(sourceDir)) {
    log('❌ Build output not found', colors.red);
    return false;
  }
  
  // Create public/docs if it doesn't exist
  exec(`mkdir -p "${outputDir}"`, rootDir, true);
  
  // Copy files
  const copyCmd = process.platform === 'win32'
    ? `xcopy "${sourceDir}" "${outputDir}" /E /I /Y /Q`
    : `cp -r "${sourceDir}/." "${outputDir}/"`;
  
  const result = exec(copyCmd, rootDir, true);
  
  if (!result.success) {
    log('❌ Failed to copy output', colors.red);
    return false;
  }
  
  log('✓ Output copied to public/docs', colors.green);
  return true;
}

async function main() {
  log('\n🚀 Building Cleanroom Labs Documentation', colors.bright + colors.blue);
  log('==========================================\n', colors.blue);
  
  const steps = [
    { name: 'Check submodule', fn: checkSubmodule },
    { name: 'Check Python', fn: checkPython },
    { name: 'Setup virtual environment', fn: setupVirtualEnv },
    { name: 'Install dependencies', fn: installDependencies },
    ...(shouldClean ? [{ name: 'Clean build', fn: cleanBuild }] : []),
    { name: 'Build documentation', fn: buildDocs },
    { name: 'Copy output', fn: copyOutput },
  ];
  
  for (const step of steps) {
    if (!step.fn()) {
      log(`\n❌ Build failed at: ${step.name}`, colors.red);
      process.exit(1);
    }
  }
  
  log('\n✅ Documentation build complete!', colors.bright + colors.green);
  log(`   Output: public/docs/index.html\n`, colors.green);
}

main().catch(error => {
  log(`\n❌ Unexpected error: ${error.message}`, colors.red);
  process.exit(1);
});
