# Mitigating Hit-Based Speculative Cache Side Channel Attacks

This project extends the [SpecLFB defense](https://www.usenix.org/system/files/sec24summer-prepub-556-cheng-xiaoyu.pdf) to mitigate hit-based speculative cache side-channel attacks. While the original SpecLFB defense focused on miss-based attacks, this implementation provides comprehensive protection against both miss-based and hit-based speculative execution vulnerabilities in out-of-order processors.

## Overview

Speculative execution attacks exploit timing differences in cache behavior during speculative execution to leak sensitive information. This project addresses both categories of speculative cache side-channel attacks:

- **Miss-Based Attacks**: Exploit cache miss timing during speculative execution
- **Hit-Based Attacks**: Exploit cache hit timing information during speculative execution (novel extension)
- **Cache Hit Filtering**: Prevents attackers from exploiting cache hit timing information
- **Comprehensive Defense**: Unified protection mechanism for both attack types

## Research Contributions

### 1. Defense Extension
- Extended SpecLFB defense from miss-based to hit-based attack mitigation
- Designed cache hit filtering mechanism for speculative execution contexts
- Maintained compatibility with existing miss-based protection

### 2. Attack Analysis
- Developed new attack strategies targeting the implemented defense
- Demonstrated bypass techniques revealing additional security considerations
- Comprehensive evaluation against both attack categories

### 3. Performance Evaluation
- Assessed defense effectiveness in simulated out-of-order environments
- Measured performance overhead across SPEC CPU benchmarks
- Analyzed security-performance trade-offs

## Prerequisites

### System Requirements

- **GCC 7**: Required for ChampSim compilation
- **Ubuntu/Linux**: Recommended development environment
- **Multi-core system**: For realistic out-of-order simulation

### Installing GCC 7

```bash
sudo apt update 
sudo add-apt-repository ppa:ubuntu-toolchain-r/test 
sudo nano /etc/apt/sources.list
```

Update the last line with:
```
deb [arch=amd64] http://archive.ubuntu.com/ubuntu focal main universe
```

Install GCC 7:
```bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/test 
sudo apt-get install gcc-7 
sudo apt-get install g++-7 

sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 0 
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 0
```

Configure alternatives (if needed):
```bash
sudo update-alternatives --config g++ 
sudo update-alternatives --config gcc
```

## Building the Project

The project uses ChampSim's comprehensive build system with custom implementations for speculative execution attack mitigation.

### Build Parameters

```bash
./build_champsim.sh ${BRANCH} ${L1I_PREF} ${L1D_PREF} ${L2C_PREF} ${LLC_PREF} ${ITLB_PREF} ${DTLB_PREF} ${STLB_PREF} ${BTB_REPL} ${L1I_REPL} ${L1D_REPL} ${L2C_REPL} ${LLC_REPL} ${ITLB_REPL} ${DTLB_REPL} ${STLB_REPL} ${NUM_CORE} ${TAIL_NAME}
```

### Build Configuration

For  evaluation:
```bash
./build_champsim.sh bimodal no no no no no no no lru lru lru lru lru lru lru lru 2 no
```



## Defense Implementation

### Core Components

#### 1. SpecLFB Extended Replacement Policy
- **Function**: Implements both miss-based and hit-based attack mitigation
- **Features**: 
  - Cache hit filtering during speculative execution
  - Miss-based attack prevention (original SpecLFB)
  - Unified defense mechanism

#### 2. Cache Hit Filtering Mechanism
- **Location**: Integrated within cache controller logic
- **Purpose**: Prevents timing-based information leakage from cache hits
- **Method**: Filters hit timing information during speculative execution windows

#### 3. Speculative Execution Tracking
- **Implementation**: Tracks speculative vs. committed execution states
- **Integration**: Works with out-of-order execution pipeline
- **Scope**: Monitors both instruction and data cache accesses

## Running Simulations

### Basic Simulation

Execute the binary directly with trace files:

```bash
bin/champsim --warmup_instructions 500000000 --simulation_instructions 500000000 ~/path/to/traces/trace_name.champsimtrace.xz
```


## Related Work and References

### Primary Reference
- **SpecLFB Original Paper**: [Cheng et al., USENIX Security 2024](https://www.usenix.org/system/files/sec24summer-prepub-556-cheng-xiaoyu.pdf)

## License and Usage

This project extends the [ChampSim](https://github.com/ChampSim/ChampSim) simulator for academic research purposes. 
