#!/usr/bin/env node

/**
 * Circuit Compilation Script for AIBPB
 * Compiles Circom circuits and generates proving/verification keys
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const CIRCUITS_DIR = path.join(__dirname, '..', 'circuits');
const BUILD_DIR = path.join(__dirname, '..', 'build');
const CIRCUITS_BUILD_DIR = path.join(BUILD_DIR, 'circuits');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function exec(command, description) {
  try {
    log(`  → ${description}...`, 'cyan');
    execSync(command, { stdio: 'inherit' });
    log(`  ✓ ${description} completed`, 'green');
    return true;
  } catch (error) {
    log(`  ✗ ${description} failed`, 'red');
    return false;
  }
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    log(`  Created directory: ${dir}`, 'yellow');
  }
}

function compileCircuit(circuitName, circuitFile) {
  log(`\nCompiling circuit: ${circuitName}`, 'cyan');

  const circuitPath = path.join(CIRCUITS_DIR, circuitFile);
  const outputDir = path.join(CIRCUITS_BUILD_DIR, circuitName);

  // Ensure directories exist
  ensureDir(outputDir);

  // Check if circuit file exists
  if (!fs.existsSync(circuitPath)) {
    log(`  Circuit file not found: ${circuitPath}`, 'red');
    return false;
  }

  // Step 1: Compile circuit to r1cs and wasm
  log('  [1/5] Compiling Circom to R1CS and WASM...', 'yellow');
  const compileCmd = `circom ${circuitPath} --r1cs --wasm --sym -o ${outputDir}`;
  if (!exec(compileCmd, 'Circuit compilation')) {
    return false;
  }

  // Step 2: Generate witness calculator info
  log('  [2/5] Circuit info...', 'yellow');
  const r1csPath = path.join(outputDir, `${circuitName}.r1cs`);
  const infoCmd = `snarkjs r1cs info ${r1csPath}`;
  if (!exec(infoCmd, 'R1CS info')) {
    log('    (Info generation failed, but continuing...)', 'yellow');
  }

  // Step 3: Generate Powers of Tau (if not exists)
  log('  [3/5] Generating Powers of Tau...', 'yellow');
  const ptauPath = path.join(BUILD_DIR, 'powersOfTau28_hez_final_10.ptau');

  if (!fs.existsSync(ptauPath)) {
    log('    Powers of Tau file not found, creating new ceremony...', 'yellow');
    const newPtauCmd = `snarkjs powersoftau new bn128 10 ${ptauPath} -v`;
    if (!exec(newPtauCmd, 'Powers of Tau new')) {
      return false;
    }

    const contributePtauCmd = `snarkjs powersoftau contribute ${ptauPath} ${ptauPath}.tmp -v -e="random entropy"`;
    if (!exec(contributePtauCmd, 'Powers of Tau contribute')) {
      return false;
    }

    // Move tmp file to final
    fs.renameSync(`${ptauPath}.tmp`, ptauPath);

    const preparePtauCmd = `snarkjs powersoftau prepare phase2 ${ptauPath} ${ptauPath}.tmp -v`;
    if (!exec(preparePtauCmd, 'Powers of Tau prepare phase2')) {
      return false;
    }

    // Move tmp file to final
    fs.renameSync(`${ptauPath}.tmp`, ptauPath);
  } else {
    log('    Using existing Powers of Tau file', 'green');
  }

  // Step 4: Generate zkey (proving and verification keys)
  log('  [4/5] Generating proving and verification keys...', 'yellow');
  const zkeyPath = path.join(outputDir, `${circuitName}.zkey`);
  const setupCmd = `snarkjs groth16 setup ${r1csPath} ${ptauPath} ${zkeyPath}`;
  if (!exec(setupCmd, 'Groth16 setup')) {
    return false;
  }

  // Step 5: Export verification key
  log('  [5/5] Exporting verification key...', 'yellow');
  const vkeyPath = path.join(outputDir, `${circuitName}_vkey.json`);
  const exportVkeyCmd = `snarkjs zkey export verificationkey ${zkeyPath} ${vkeyPath}`;
  if (!exec(exportVkeyCmd, 'Verification key export')) {
    return false;
  }

  log(`\n✓ Circuit ${circuitName} compiled successfully!`, 'green');
  log(`  Output directory: ${outputDir}`, 'cyan');

  return true;
}

function main() {
  log('='.repeat(80), 'cyan');
  log('AIBPB Circuit Compilation'.center(80), 'cyan');
  log('='.repeat(80), 'cyan');

  // Ensure build directories exist
  ensureDir(BUILD_DIR);
  ensureDir(CIRCUITS_BUILD_DIR);

  // Find all .circom files in circuits directory
  const circuits = fs.readdirSync(CIRCUITS_DIR)
    .filter(file => file.endsWith('.circom'))
    .map(file => ({
      name: path.basename(file, '.circom'),
      file: file
    }));

  if (circuits.length === 0) {
    log('\nNo circuit files found in circuits directory!', 'red');
    process.exit(1);
  }

  log(`\nFound ${circuits.length} circuit(s) to compile:\n`, 'yellow');
  circuits.forEach(c => log(`  - ${c.name}`, 'cyan'));

  // Compile each circuit
  let successCount = 0;
  for (const circuit of circuits) {
    if (compileCircuit(circuit.name, circuit.file)) {
      successCount++;
    }
  }

  // Summary
  log('\n' + '='.repeat(80), 'cyan');
  log(`Compilation complete: ${successCount}/${circuits.length} successful`,
      successCount === circuits.length ? 'green' : 'yellow');
  log('='.repeat(80), 'cyan');

  process.exit(successCount === circuits.length ? 0 : 1);
}

// Helper function for string padding (center)
String.prototype.center = function(width) {
  const padding = Math.max(0, width - this.length);
  const left = Math.floor(padding / 2);
  const right = padding - left;
  return ' '.repeat(left) + this + ' '.repeat(right);
};

// Run main function
if (require.main === module) {
  main();
}

module.exports = { compileCircuit };
