---
title: GPU Exercises 4
permalink: /GPU/Exercise4
nav_order: 16
parent: "GPU Exercises"
grand_parent: "Exercises"
---
<div id="top"></div>

<div align="center">
  <a href="https://universityofsussex-rc.github.io/Workshops/">
    <img src="https://universityofsussex-rc.github.io/Workshops/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">GPU Exercises #4</h3>
  <p align="center">
    Your own code: run it as a well-behaved GPU job, check it, and scale up.
  </p>
    <a href="https://universityofsussex-rc.github.io/Workshops/"><strong>Go Back to Splash »</strong></a>
    <br />
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Exercises</summary>
  <ol>
    <li><a href="#checklist-before-you-submit">Checklist before you submit</a></li>
    <li><a href="#run-your-code">Run your code</a></li>
    <li><a href="#check-how-it-went">Check how it went</a></li>
    <li><a href="#scale-up-with-a-job-array">Scale up with a job array</a></li>
    <li><a href="#no-code-of-your-own">No code of your own?</a></li>
    <li><a href="#wrap-up">Wrap up</a></li>
  </ol>
</details>

<p align="right">(<a href="#top">back to top</a>)</p>

**Time:** the remaining time in the session. This exercise is deliberately open: bring your own code, or use one of the suggestions at the end.

## Checklist before you submit

Work through this **in a CPU interactive session** (`srun -p <CPU_PARTITION> --pty bash`):

- [ ] **Does your code use a GPU?** Look for CUDA, GPU or NVIDIA in its documentation, or for a library such as PyTorch, TensorFlow, CuPy, Numba or JAX. If it does not, the GPU will sit idle.
- [ ] **Do you know which modules and packages it needs, with versions?** Write them down. Do not rely on default versions.
- [ ] **Is everything installed already?** Do downloads and installs now. GPU batch jobs should not need the internet.
- [ ] **Does it run on a tiny input?** Test on the CPU first, if your code supports it.
- [ ] **Where are the input and output files?** Keep them on Lustre, and write results somewhere you will not lose them.
- [ ] **How long will it take?** If you do not know, run a very small case first and estimate.

## Run your code

1. Copy the template and open it:

    ```bash
    cp byo_gpu.job my_gpu_job.job
    ```

2. Edit the lines marked `<-- CHANGE`: the job name, a realistic `--time` (keep it to 10 minutes or less today), your modules and environment, and the command that runs your code.

3. Keep `--gres=gpu:1`. **One GPU per job**: 6 GPUs are shared by the whole room.

4. Make sure your code reports whether it found a GPU. In Python, for example:

    ```python
    import torch
    print("CUDA available:", torch.cuda.is_available())
    ```

5. Submit and watch:

    ```bash
    sbatch my_gpu_job.job
    squeue --me
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Check how it went

A job that *finished* is not necessarily a job that *used the GPU well*. Check:

1. **Did it finish cleanly?**

    ```bash
    sacct -j <jobid> --format=JobID,JobName,Partition,Elapsed,MaxRSS,State,ExitCode
    ```

    `State` should be `COMPLETED` and `ExitCode` `0:0`. `TIMEOUT` means it hit `--time`. `OUT_OF_MEMORY` means it ran out of CPU memory, so raise `--mem`.

2. **Was the GPU busy?** Add a usage log to your script, as in [GPU Exercises 2]({{ site.baseurl }}{% link exercises/gpu/Exercise2/README.md %}):

    ```bash
    nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used --format=csv -l 2 > gpu_usage-$SLURM_JOB_ID.csv &
    MON_PID=$!
    python my_script.py
    kill $MON_PID
    ```

    Utilisation that stays low usually means the code is waiting on the CPU or on data loading, or the input is too small for the GPU to help.

3. **How much GPU memory did it use?** If the peak is close to the total, a slightly bigger input will fail. If it is tiny, you may be able to do more work per job.

4. **Was the time limit sensible?** Compare `Elapsed` with your `--time`. A limit 2 to 3 times the real run time is comfortable. A very long limit makes the job wait longer to start.

<p align="right">(<a href="#top">back to top</a>)</p>

## Scale up with a job array

To run the same code with different inputs (seeds, parameters, data files), use a **job array** instead of submitting jobs by hand or in a loop. The example `gpu_array.job` runs four tasks, two at a time, one GPU each:

```bash
#SBATCH --array=1-4%2
#SBATCH --output=gpu_array-%A_%a.out
...
python my_script.py --seed $SLURM_ARRAY_TASK_ID
```

1. Copy `gpu_array.job`, fill in the partition and module, and point it at your script.
2. Make your script use the task number (`$SLURM_ARRAY_TASK_ID`) to choose its input.
3. Submit it. In `squeue --me`, how are the array tasks shown?
4. **Etiquette:** the `%2` limits how many tasks run at once. On a busy shared system, always set one.

<p align="right">(<a href="#top">back to top</a>)</p>

## No code of your own?

Pick one of these:

- **Change the benchmark.** In `gpu_check.py`, add a second operation (for example an element-wise `torch.sin`) and time it on the CPU and GPU. Which gets more benefit from the GPU, matrix multiply or element-wise maths? Why?
- **Try a different matrix size sweep** as a job array, using `$SLURM_ARRAY_TASK_ID` to pick `--n`.
- **Extend the CUDA program.** In `vector_add.cu`, time the memory copies as well as the kernel. How much of the total time is spent moving data?
- **Explore the framework.** Use the PyTorch tutorials to train a very small model on the GPU for a few epochs (keep the run under 10 minutes), and log its speed.

<p align="right">(<a href="#top">back to top</a>)</p>

## Wrap up

Before you leave:

- [ ] Copy anything you want to keep from your job folders into your own storage.
- [ ] `scancel` any jobs you no longer need: `squeue --me` to check.
- [ ] Remove environments you do not need: `conda env remove -p <path>` and `conda clean --all`.
- [ ] Note down which of the checklist points caught you out. That is where to look first next time something fails.

**Where next?**

- The [Advanced Exercises]({{ site.baseurl }}{% link exercises/Software/Exercise1/README.md %}) cover installing your own software and EasyBuild.
- Ask questions in the Slack channel, or raise a request through the ITS Help Desk.
- Bigger GPU projects: talk to the Research Computing team about limits, partitions and access.

<p align="right">(<a href="#top">back to top</a>)</p>
