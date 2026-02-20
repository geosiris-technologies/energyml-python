import logging
import os
import shutil
import sys
import time
from typing import Optional

from energyml.utils.epc_stream import EpcStreamReader, RelsUpdateMode
from energyml.utils.epc import Epc
from energyml.utils.epc_utils import update_prop_kind_dict_cache


def reexport_stream_seq(filepath: str, output_folder: Optional[str] = None):
    path_seq = filepath.replace(".epc", "_stream_seq.epc")
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        path_seq = f"{output_folder}/{path_seq.split('/')[-1]}"
    shutil.copy(filepath, path_seq)
    with EpcStreamReader(
        epc_file_path=path_seq, enable_parallel_rels=False, rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE
    ) as reader:
        pass  # Just open and close to trigger rels computation on close


def reexport_stream_parallel(filepath: str, output_folder: Optional[str] = None):
    path_parallel = filepath.replace(".epc", "_stream_parallel.epc")
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        path_parallel = f"{output_folder}/{path_parallel.split('/')[-1]}"
    shutil.copy(filepath, path_parallel)
    with EpcStreamReader(
        epc_file_path=path_parallel, enable_parallel_rels=True, rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE
    ) as reader:
        pass  # Just open and close to trigger rels computation on close


def reexport_in_memory(filepath: str, output_folder: Optional[str] = None):
    path_in_memory = filepath.replace(".epc", "_in_memory.epc")
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        path_in_memory = f"{output_folder}/{path_in_memory.split('/')[-1]}"
    epc = Epc.read_file(epc_file_path=filepath, read_rels_from_files=False, recompute_rels=False)

    if os.path.exists(path_in_memory):
        os.remove(path_in_memory)
    epc.export_file(path_in_memory)


def reexport_in_memory_par_read(filepath: str, output_folder: Optional[str] = None):
    path_in_memory = filepath.replace(".epc", "_in_memory_par_read.epc")
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        path_in_memory = f"{output_folder}/{path_in_memory.split('/')[-1]}"
    epc = Epc.read_file(epc_file_path=filepath, read_rels_from_files=False, read_parallel=True, recompute_rels=False)

    if os.path.exists(path_in_memory):
        os.remove(path_in_memory)
    epc.export_file(path_in_memory, parallel=True)


def time_comparison(
    filepath: str,
    output_folder: Optional[str] = None,
    skip_sequential_stream: bool = True,
    skip_parallel_stream: bool = True,
):
    """Compare performance of different EPC reexport methods."""
    print(f"\n{'=' * 70}")
    print(f"Performance Comparison: {filepath.split('/')[-1]}")
    print(f"{'=' * 70}\n")

    results = []

    # Test 1: In-Memory
    print("⏳ Testing In-Memory EPC processing...")
    start = time.perf_counter()
    reexport_in_memory(filepath, output_folder)
    elapsed_inmem = time.perf_counter() - start
    results.append(("In-Memory (Epc)", elapsed_inmem))
    print(f"   ✓ Completed in {elapsed_inmem:.3f}s\n")

    # Test 1b: In-Memory with Parallel Read
    print("⏳ Testing In-Memory EPC processing with Parallel Read...")
    start = time.perf_counter()
    reexport_in_memory_par_read(filepath, output_folder)
    elapsed_inmem_par = time.perf_counter() - start
    results.append(("In-Memory (Epc) Parallel Read", elapsed_inmem_par))
    print(f"   ✓ Completed in {elapsed_inmem_par:.3f}s\n")

    if not skip_sequential_stream:
        # Test 2: Streaming Sequential
        print("⏳ Testing Streaming Sequential processing...")
        start = time.perf_counter()
        reexport_stream_seq(filepath, output_folder)
        elapsed_seq = time.perf_counter() - start
        results.append(("Stream Sequential", elapsed_seq))
        print(f"   ✓ Completed in {elapsed_seq:.3f}s\n")

    # Test 3: Streaming Parallel
    if not skip_parallel_stream:
        print("⏳ Testing Streaming Parallel processing...")
        start = time.perf_counter()
        reexport_stream_parallel(filepath, output_folder)
        elapsed_parallel = time.perf_counter() - start
        results.append(("Stream Parallel", elapsed_parallel))
        print(f"   ✓ Completed in {elapsed_parallel:.3f}s\n")

    # Calculate speedups
    results_sorted = sorted(results, key=lambda x: x[1])
    fastest_time = results_sorted[0][1]

    # Print fancy table
    print(f"\n{'=' * 70}")
    print(f"{'PERFORMANCE RESULTS':^70}")
    print(f"{'=' * 70}")
    print(f"{'Method':<25} {'Time (s)':>12} {'Speedup':>12} {'Status':>15}")
    print(f"{'-' * 70}")

    for method, elapsed in results_sorted:
        speedup = fastest_time / elapsed
        if speedup >= 0.95:  # Fastest
            status = "🏆 FASTEST"
        elif speedup >= 0.8:
            status = "✓ Good"
        else:
            status = "○ Slower"

        print(f"{method:<25} {elapsed:>12.3f} {speedup:>12.2f}x {status:>15}")

    print(f"{'=' * 70}")

    # Summary
    fastest_method = results_sorted[0][0]
    slowest_method = results_sorted[-1][0]
    speedup_factor = results_sorted[-1][1] / fastest_time

    print(f"\n📊 Summary:")
    print(f"   • Fastest: {fastest_method} ({fastest_time:.3f}s)")
    print(f"   • Slowest: {slowest_method} ({results_sorted[-1][1]:.3f}s)")
    print(f"   • Overall speedup: {speedup_factor:.2f}x faster\n")


def recompute_rels(epc_file_path: str):
    with EpcStreamReader(
        epc_file_path=epc_file_path, enable_parallel_rels=True, rels_update_mode=RelsUpdateMode.UPDATE_ON_CLOSE
    ) as reader:
        pass  # Just open and close to trigger rels computation on close


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    update_prop_kind_dict_cache()

    # time_comparison(
    #     filepath=sys.argv[1] if len(sys.argv) > 1 else "rc/epc/testingPackageCpp22.epc",
    #     output_folder="rc/performance_results",
    # )

    # time_comparison(
    #     filepath=sys.argv[1] if len(sys.argv) > 1 else "rc/epc/80wells_surf.epc", output_folder="rc/performance_results"
    # )

    # time_comparison(
    #     filepath=sys.argv[1] if len(sys.argv) > 1 else "wip/failingData/fix/sample_mini_firp_201_norels_with_media.epc",
    #     output_folder="rc/performance_results",
    # )

    recompute_rels("C:/Users/Cryptaro/Downloads/Galaxy384-[[Output] EPC file pointset extraction].epc")
