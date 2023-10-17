# RUN: env ARTIQ_DUMP_LLVM=%t %python -m artiq.compiler.testbench.embedding +compile %s
# RUN: OutputCheck %s --file-to-check=%t.ll

from artiq.language.core import *
from artiq.language.types import *

class A:
    @subkernel(destination=1)
    def sk(self, a):
        pass

    @kernel
    def kernel_entrypoint(self):
        # CHECK: call void @subkernel_load_run\(i32 1, i1 true\), !dbg !.
        # CHECK: call void @subkernel_send_message\(i32 1, i8 1, .*\), !dbg !.
        self.sk(1)

a = A()

@kernel
def entrypoint():
    a.kernel_entrypoint()

# CHECK-L: declare void @subkernel_load_run(i32, i1) local_unnamed_addr
# CHECK-L: declare void @subkernel_send_message(i32, i8, { i8*, i32 }*, i8**) local_unnamed_addr
