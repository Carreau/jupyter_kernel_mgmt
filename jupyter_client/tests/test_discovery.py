import sys

from jupyter_client import discovery
from jupyter_client.launcher2 import KernelLauncher

def test_ipykernel_provider():
    import ipykernel  # Fail clearly if ipykernel not installed
    ikf = discovery.IPykernelProvider()

    res = list(ikf.find_kernels())
    assert len(res) == 1, res
    id, info = res[0]
    assert id == 'kernel'
    assert info['argv'][0] == sys.executable

class DummyKernelProvider(discovery.KernelProviderBase):
    """A dummy kernel provider for testing KernelFinder"""
    id = 'dummy'

    def find_kernels(self):
        yield 'sample', {'argv': ['dummy_kernel']}

    def launch(self, name, cwd=None):
        return DummyKernelLauncher()

class DummyKernelLauncher(KernelLauncher):
    def is_alive(self):
        """Check whether the kernel is currently alive (e.g. the process exists)
        """
        return True

    def wait(self):
        """Wait for the kernel process to exit.
        """
        return 0

    def signal(self, signum):
        """Send a signal to the kernel."""
        pass

    def get_connection_info(self):
        """Return a dictionary of connection information"""
        return {}

def test_meta_kernel_finder():
    kf = discovery.KernelFinder(providers=[DummyKernelProvider()])
    assert list(kf.find_kernels()) == \
        [('dummy/sample', {'argv': ['dummy_kernel']})]

    launcher = kf.launch('dummy/sample')
    assert isinstance(launcher, DummyKernelLauncher)