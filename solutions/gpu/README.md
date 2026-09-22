---
title: GPU Exercises Solutions
permalink: /GPU/Solutions
nav_order: 17
parent: "GPU Exercises"
grand_parent: "Exercises"
---
<div id="top"></div>

<div align="center">
  <a href="https://universityofsussex-rc.github.io/Workshops/">
    <img src="https://universityofsussex-rc.github.io/Workshops/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GPU Exercises: Solutions</h3>
  <p align="center">
    Worked answers to every open-ended question in GPU Exercises 1 to 4.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Contents</summary>
  <ol>
    <li><a href="#how-to-use-this-page">How to use this page</a></li>
    <li><a href="#exercise-1-your-first-gpu-job">Exercise 1: your first GPU job</a></li>
    <li><a href="#exercise-2-python-on-the-gpu">Exercise 2: Python on the GPU</a></li>
    <li><a href="#exercise-3-cuda-modules-and-compiling">Exercise 3: CUDA modules and compiling</a></li>
    <li><a href="#exercise-4-your-own-code">Exercise 4: your own code</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

## How to use this page

Most of the questions in these exercises don't have one fixed answer - they ask you to read your *own* job output and explain what you see. For those, this page gives the **reasoning and the pattern to look for**, not a number to copy, because your number depends on which GPU you were given and what you ran. Questions that do have one correct answer (fix this line, what code do you add) are given in full.

Section headings below match the exercise they answer, so you can jump to the same point in each.

<p align="right">(<a href="#top">back to top</a>)</p>

## Exercise 1: your first GPU job

*From [GPU Exercises 1]({{ site.baseurl }}{% link exercises/gpu/Exercise1/README.md %}).*

**Write the job script**

- *Which line asks Slurm for a GPU? What would happen if you deleted it?*
  `#SBATCH --gres=gpu:<GPU_FLAVOR>:1` (on Brighton, `#SBATCH --gres=gpu:RTX:1`). Delete it and the job still runs, but as an ordinary CPU allocation with no GPU attached - `nvidia-smi` reports something like `No devices were found`, because Slurm never gave the job a GPU to see.

- *What does `gpu:1` (no flavour) mean? When would you name the flavour?*
  `gpu:1` means "any one GPU in this partition, whichever flavour it is." Name the flavour when your code depends on the CUDA version or GPU architecture - compiled CUDA code, a specific CUDA toolkit, or a framework build that only contains code for one architecture. If your code just needs "a GPU" and doesn't care which, `gpu:1` is enough.

- *Why is `--time` set to only 5 minutes?*
  The script only prints `nvidia-smi` output, so it finishes in seconds. A short, realistic `--time` starts sooner (Slurm can fit it into a gap in the schedule) and is a courtesy on a workshop partition with only 6 GPUs shared by the room.

**Read the results**

- *Which compute node did the job run on?*
  Read it from the first line of the output - `echo "Job $SLURM_JOB_ID on $(hostname) at $(date)"` prints the hostname directly.

- *Which GPU model did you get, and how much memory does it have?*
  Read the `Name` and `memory.total` fields from the `nvidia-smi` output. This is genuinely per-allocation - write down what your own job reports, since you'll need that memory figure again in Exercise 2 (question 5, below).

- *What is the GPU's compute capability?*
  On the `brighton` partition, every node is RTX, so you should see **12.0** (`sm_120`) - a newer architecture than the A40's 8.6. That's why Exercise 2 and Exercise 3 both make a point of matching your CUDA build and compile target to the architecture you were given.

- *What CUDA version does `nvidia-smi` report in its header? What does that number mean?*
  This is the newest CUDA version the GPU's **driver** supports - a ceiling, not what's actually loaded in your shell. On Artemis this should be 12.9 or newer, which is why the `CUDA/12.9.1` module (new enough for `sm_120`) works here.

- *What was the GPU doing when you ran `nvidia-smi`?*
  Idle: 0% `GPU-Util` and close to 0 MiB used. The script never launches any GPU work, so there's nothing there to see yet - this is the expected, correct answer, not a sign anything went wrong.

- *Add two lines that print the working directory and the number of CPUs (`$SLURM_CPUS_ON_NODE`):*

  ```bash
  echo "Working directory: $(pwd)"
  echo "CPUs on this node: $SLURM_CPUS_ON_NODE"
  ```

**Job Composer: repair the `slurm_gpu` template**

The exact mistakes depend on the template's current content, but the checklist is always the same three things: the **partition** must be `brighton`, the **`--gres`** line must use the `gpu:<flavour>:<number>` syntax (not an older or malformed form), and it should ask for exactly **one GPU** (`gpu:RTX:1`), not more. If the fixed job still fails, compare it line-by-line against `gpu_test.job` from earlier in this exercise - that script is a known-working reference.

**Extension: what happens without a GPU request?**

- *What does `nvidia-smi` say now?* The same as if you'd never asked for a GPU at all: no device is visible (e.g. `No devices were found`), because `CUDA_VISIBLE_DEVICES` is empty for the job.
- *Why does this matter for your own code?* Many frameworks silently fall back to the CPU instead of erroring when no GPU is visible. A job can "work" - just slowly, and without you noticing - if you don't explicitly check and log whether a GPU was found (as `gpu_check.py` does in Exercise 2).

**Extension: `gpu:1` or a named flavour?**

- *Why might the GPU name not match, on a partition with more than one flavour?* `gpu:1` picks any available GPU in the partition. On a partition that mixes A40 and RTX nodes, two `gpu:1` jobs submitted at different times could land on different node types and come back with different GPU names, different memory, and different compute capabilities. On `brighton` every node is RTX, so `gpu:1` and `gpu:RTX:1` always agree - but naming the flavour is what makes that guaranteed rather than incidental.

<p align="right">(<a href="#top">back to top</a>)</p>

## Exercise 2: Python on the GPU

*From [GPU Exercises 2]({{ site.baseurl }}{% link exercises/gpu/Exercise2/README.md %}).*

**Understand the results**

- *Was CUDA available? Which GPU did PyTorch find? Did `Build supports` include your architecture?*
  With a CUDA-enabled build matching your GPU, `CUDA available` should be `True`, the GPU name should match Exercise 1, and `sm_120` should appear in the `Build supports` list. A `WARNING` means the installed build doesn't contain code for `sm_120` - go back and install a newer build (Option B, step 3).

- *How much faster was the GPU than the CPU?*
  Expect a large speed-up - commonly somewhere in the tens-of-times range for an 8192×8192 matrix multiply, though the exact figure depends on your GPU and the CPU it's compared against. The reasoning matters more than the number: dense matrix multiplication is highly parallel and exactly the kind of workload a GPU is built for, so a big speed-up here is the expected, correct result.

- *When did GPU utilisation rise, and what was it doing the rest of the time?*
  Utilisation should spike during the timed `matmul` repeats and sit near 0% otherwise - while Python builds the random matrices, copies them to the GPU, and handles other overhead. A GPU that's busy only in short bursts, with idle time either side, is normal for a script this small.

- *Change `--n` to 512, 2048, 16384: how does the speed-up change, and why do small problems benefit less?*
  Speed-up should grow as `--n` grows. At `n=512` there's very little arithmetic to do, so the fixed costs - launching the kernel, copying data to and from the GPU - can dominate the total time, and the GPU may barely beat the CPU or even lose to it. At `n=16384` there's far more arithmetic per byte moved, so that fixed overhead becomes a small fraction of the total and the GPU's raw throughput advantage shows through.

- *Roughly how large can `n` be before `CUDA out of memory`?*
  Work it out from your GPU's memory (from Exercise 1) rather than guessing: the script holds three `n`×`n` float32 matrices on the GPU (the two inputs and the result), and each float32 element is 4 bytes, so it needs roughly `3 × n² × 4` bytes, plus some working memory PyTorch reserves on top. Solve `3 × n² × 4 < (your GPU's free memory in bytes)` for `n` as a rough ceiling - real headroom will be a bit lower once PyTorch's own overhead is included.

<p align="right">(<a href="#top">back to top</a>)</p>

## Exercise 3: CUDA modules and compiling

*From [GPU Exercises 3]({{ site.baseurl }}{% link exercises/gpu/Exercise3/README.md %}).*

**Find and understand CUDA modules**

- *Split `NCCL/2.27.7-GCCcore-14.3.0-CUDA-12.9.1` into software / version / toolchain / CUDA version:*
  Software = `NCCL`, version = `2.27.7`, toolchain = `GCCcore-14.3.0`, CUDA version = `12.9.1`.

- *Do the same for two other modules from `module avail CUDA`:*
  The names on your own system will differ, but the pattern is always `<Software>/<version>-<toolchain>-<suffix>`, and any `-CUDA-<version>` segment in the suffix is the CUDA version that module was built against. Read each one left to right in the same four pieces as the NCCL example above.

- *What warning does Module give when you load a second, conflicting CUDA version?*
  Something in the family of `Lmod is automatically replacing "CUDA/12.9.1" with "CUDA/<other version>"`, or a note that other modules were reloaded with a version change. It's Lmod telling you it swapped out part of your environment to satisfy the new module - exactly the silent, order-dependent surprise that `module purge` before loading a fresh set avoids.

**Compile and run CUDA C**

- *Did it print `PASSED`? What GPU did it use, and what bandwidth did it achieve?*
  `PASSED` is expected: the program checks its own answer (every element should equal 3.0) and only prints `FAILED` if something is wrong. The GPU name matches your allocation from Exercise 1. There's no single "correct" bandwidth figure, but as a sanity check it should be a sizeable fraction of your GPU's rated memory bandwidth - a number close to zero would suggest something is misconfigured (for example, running on the wrong device) rather than a genuine result.

- *Does the speed change when you target `-arch=sm_<yours>` explicitly?*
  Often little or no visible change for this program. `vector_add` is **memory-bandwidth-bound**, not compute-bound - it does one addition per element it reads, so its speed is limited by how fast data moves, not by arithmetic throughput, and that doesn't change much with the compile target. What naming the architecture *does* guarantee is that the binary contains code for your GPU at all, rather than relying on the toolkit's default and (depending on the toolkit) a slower first-run JIT step or an outright failure to run on a newer architecture.

- *Set `threads = 2048` in `vector_add.cu`: what error do you get?*
  A kernel launch failure, typically reported as something like `invalid configuration argument`. Almost all current NVIDIA GPUs cap threads per block at 1024, so requesting 2048 is invalid before the kernel even starts. `CHECK(cudaGetLastError())` is what surfaces this - without it, the launch would fail silently and the program would report `FAILED` (or hang) with no explanation.

**Benchmark: mixbench**

- *Where does the GPU stop being memory-bound and start being compute-bound?*
  Look for the point where the `GB/s` curve flattens out (memory bandwidth is maxed) while `GFLOPS` keeps climbing as more arithmetic is done per byte moved - that crossover is the "ridge point" in roofline terms. Below it, performance is capped by how fast data can move (GB/s stays roughly flat, GFLOPS rises with more work per byte); above it, performance is capped by arithmetic throughput (GFLOPS plateaus near the GPU's peak, GB/s falls off as less new data is needed per calculation). The exact crossover point is specific to your GPU, but the shape of the curve is the thing to look for.

<p align="right">(<a href="#top">back to top</a>)</p>

## Exercise 4: your own code

*From [GPU Exercises 4]({{ site.baseurl }}{% link exercises/gpu/Exercise4/README.md %}).*

Exercise 4 is intentionally open (your own code), so most of it has no single answer. The exceptions:

**Scale up with a job array**

- *In `squeue --me`, how are the array tasks shown?*
  As one entry per task in the form `<jobid>_<taskindex>` (for example `12345_1`, `12345_2`, ...) rather than as separate, unrelated job IDs. Tasks beyond your `%` concurrency limit show as pending until a running task finishes and frees a slot.

**No code of your own? (extension prompts)**

- *Add `torch.sin` alongside the matrix multiply: which benefits more from the GPU, and why?*
  Matrix multiply benefits far more. It's compute-bound and highly reused - for an `n`×`n` multiply there are `O(n³)` operations over `O(n²)` data, and libraries like cuBLAS are heavily optimised for exactly this shape of work. `torch.sin` is elementwise: `O(n²)` operations over `O(n²)` data, one operation per element read, so it's memory-bandwidth-bound in the same way `vector_add.cu` is. It will still be faster on the GPU than the CPU, just by a much smaller margin than the matrix multiply.

- *Time the memory copies in `vector_add.cu` as well as the kernel: how much of the total time is data movement?*
  For a kernel this simple, expect the host-to-device and device-to-host copies to account for a large share of the total time - often more than the kernel itself, especially at smaller `n`. This is the general lesson behind "prepare on CPU, run on GPU" from the workshop overview: for small, simple kernels, moving data is frequently the expensive part, not the computation.

<p align="right">(<a href="#top">back to top</a>)</p>
