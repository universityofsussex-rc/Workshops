---
title: GPU Exercises 3
permalink: /GPU/Exercise3
nav_order: 15
parent: "GPU Exercises"
grand_parent: "Exercises"
---
<div id="top"></div>

<div align="center">
  <a href="https://universityofsussex-rc.github.io/Workshops/">
    <img src="https://universityofsussex-rc.github.io/Workshops/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GPU Exercises #3</h3>
  <p align="center">
    CUDA modules, compiling CUDA C, and a GPU benchmark.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Exercises</summary>
  <ol>
    <li><a href="#find-and-understand-cuda-modules">Find and understand CUDA modules</a></li>
    <li><a href="#compile-and-run-cuda-c">Compile and run CUDA C</a></li>
    <li><a href="#benchmark-mixbench">Benchmark: mixbench</a></li>
    <li><a href="#installing-software">Installing software</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

**Time:** about 25 minutes. Do [GPU Exercises 1]({{ site.baseurl }}{% link exercises/gpu/Exercise1/README.md %}) first. You need the GPU's **compute capability** that you noted there.

Start (or return to) a CPU session in your workshop folder:

```bash
srun -p <CPU_PARTITION> --pty bash
cd ~/HPC-Workshop/workdir/GPU
```

## Find and understand CUDA modules

1. List what is installed, and search for versions:

    ```bash
    module avail CUDA
    module spider CUDA
    ```

2. Module names encode how software was built. Here is a real GPU module name from Artemis:

    ```text
    NCCL/2.27.7-GCCcore-14.3.0-CUDA-12.9.1
    ```

    Split it into: **software**, **version**, **toolchain**, **CUDA version**. NCCL is NVIDIA's library for communication between GPUs, so this one is used by multi-GPU software rather than loaded on its own. Then pick two other modules from `module avail CUDA` and do the same.

3. Check what a module would change before you load it:

    ```bash
    module display <CUDA_MODULE>
    ```

4. Load a clean environment and confirm the compiler is found:

    ```bash
    module purge
    module load <CUDA_MODULE>
    module list
    which nvcc
    nvcc --version
    ```

    *TODO(RC): confirm `nvcc` is available in a CPU session. If it is not, the compile step below still works because the job script compiles on the GPU node.*

5. Try loading a second, different CUDA version on top. What warning does Module give you? This is why we `module purge` first and never mix versions.

<p align="right">(<a href="#top">back to top</a>)</p>

## Compile and run CUDA C

`vector_add.cu` is a small CUDA program that adds two vectors on the GPU. Read it first:

- `__global__ void vector_add(...)` is the **kernel**: code that runs on the GPU. Each GPU thread adds one pair of numbers.
- `cudaMalloc` and `cudaMemcpy` allocate memory on the GPU and copy data across. This copying has a cost.
- `vector_add<<<blocks, threads>>>(...)` launches the kernel with many threads.
- The program checks its own answer and reports the time and memory bandwidth.

Now run it as a GPU batch job. Open `cuda_vector_add.job`:

```bash
#!/bin/bash
#SBATCH --job-name=cuda_vector_add
#SBATCH --partition=<GPU_PARTITION>
#SBATCH --gres=gpu:1
#SBATCH --time=00:05:00
#SBATCH --output=cuda_vector_add-%j.out

module purge
module load <CUDA_MODULE>

nvcc --version
nvcc -O2 -o vector_add vector_add.cu

./vector_add
./vector_add 100000000
```

1. Replace `<GPU_PARTITION>` and `<CUDA_MODULE>`, then `sbatch cuda_vector_add.job`.
2. Read the output. Did it print `PASSED`? What GPU did it use? What memory bandwidth did it achieve?
3. **Targeting your GPU:** `nvcc` builds for a default architecture. Add your GPU's compute capability to the compile line, for example `-arch=sm_86` for an A40 (compute capability 8.6: remove the dot). Use the value you noted in Exercise 1 for your own GPU. Does the speed change?
   - **A CUDA toolkit can only target architectures it knows about.** If your GPU is newer than the toolkit (for example an RTX with compute capability 12.0 needs CUDA 12.8 or newer), `nvcc` will reject the `-arch` value. Load a newer CUDA module.
   - **A binary built for one architecture will not necessarily run on another.** That is why, in your own jobs, you name the GPU flavour when you compile for a specific one.
4. **Break it on purpose:** change `threads` in `vector_add.cu` to `2048` and resubmit. What error do you get? (Hint: CUDA limits the number of threads per block, and `CHECK(cudaGetLastError())` reports the launch failure.)

<p align="right">(<a href="#top">back to top</a>)</p>

## Benchmark: mixbench

[mixbench](https://github.com/ekondis/mixbench) measures how fast a GPU can do arithmetic and move memory across different workloads. Follow the steps in the project's README for the CUDA build; in outline:

1. In your **CPU session** (internet is available), download the code:

    ```bash
    git clone https://github.com/ekondis/mixbench
    cd mixbench
    ```

2. Write a job script (start from `cuda_vector_add.job`) that loads a CUDA module and CMake, builds the CUDA version, and runs it. The build looks like this (check the README, as the steps can change between versions):

    ```bash
    module purge
    module load <CUDA_MODULE> CMake/<version>
    cd mixbench/mixbench-cuda
    mkdir -p build && cd build
    cmake ../
    make
    ./mixbench-cuda
    ```

3. Submit it, then read the output. mixbench reports **GFLOPS** (arithmetic speed) and **GB/s** (memory speed) as the amount of arithmetic per byte of memory changes. Where does the GPU stop being limited by memory and start being limited by arithmetic?
4. If the project provides a CPU version, build and run it the same way in a CPU job and compare.

*TODO(RC): confirm the CMake module name and test the build on Artemis before the workshop.*

<p align="right">(<a href="#top">back to top</a>)</p>

## Installing software

Users should always **request software through the ITS help portal first**. If it is missing, self-install is possible for advanced users. See [Advanced Exercises 1]({{ site.baseurl }}{% link exercises/Software/Exercise1/README.md %}) for building software from source into Lustre and using EasyBuild. Key points for GPU software:

- Install into **Lustre** user storage, not your home directory.
- Use a specific compiler toolchain, and keep the CUDA version consistent with it.
- Build on the type of node it will run on. Software built on one node type may not run on another.

Next: [GPU Exercises 4]({{ site.baseurl }}{% link exercises/gpu/Exercise4/README.md %}).

<p align="right">(<a href="#top">back to top</a>)</p>
