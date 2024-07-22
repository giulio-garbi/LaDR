# Launch the tool
```
git clone https://github.com/giulio-garbi/LaDR.git
cd LaDR
python3 ./lazycseq.py -i </full/path/to/testcase.c> --unwind <nr_unwinds> --rounds <nr_rounds> --mydr 
```
The final answer will be `true` if no data-race is found, `false` viceversa.
Make sure that the directories `LaDR` and `/full/path/to` are writable.

# Launch the tool and get the trace
```
git clone https://github.com/giulio-garbi/LaDR.git
cd LaDR
python3 ./lazycseq.py -i </full/path/to/testcase.c> --unwind <nr_unwinds> --rounds <nr_rounds> --mydr --seq
./cbmc  --unwind 1 --no-unwinding-assertions --32 </full/path/to/_csdr_testcase.c> --stop-on-fail --nondet-static-matching '.*_nondet_.*'
```
Note: run `cbmc` on the instrumented version of the testcase, which is stored in the original directory in the file `_csdr_testcase.c` (if the original file was `testcase.c`).