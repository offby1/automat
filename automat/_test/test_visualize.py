
import os
import subprocess
from unittest import TestCase, skipIf

from .._methodical import MethodicalMachine

def isGraphvizInstalled():
    """
    Is graphviz installed?
    """
    r, w = os.pipe()
    os.close(w)
    try:
        return not subprocess.call("dot", stdin=r)
    except:
        return False
    finally:
        os.close(r)



def sampleMachine():
    """
    Create a sample L{MethodicalMachine} with some sample states.
    """
    mm = MethodicalMachine()
    @mm.state(initial=True)
    def begin(result):
        pass
    @mm.state()
    def end(result):
        pass
    @mm.input()
    def go(result):
        pass
    @mm.output()
    def out(result):
        pass
    mm.transitions([(begin, go, end, [out])])
    return mm



@skipIf(not isGraphvizInstalled(), "Graphviz is not installed.")
class IntegrationTests(TestCase):
    """
    Tests which make sure Graphviz can understand the output produced by
    Automat.
    """

    def test_validGraphviz(self):
        """
        L{graphviz} emits valid graphviz data.
        """
        p = subprocess.Popen("dot", stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        out, err = p.communicate("".join(sampleMachine().graphviz()))
        self.assertEqual(p.returncode, 0)


class SpotChecks(TestCase):
    """
    Tests to make sure that the output contains salient features of the machine
    being generated.
    """

    def test_containsMachineFeatures(self):
        """
        The output of L{graphviz} should contain the names of the states,
        inputs, outputs in the state machine.
        """
        gvout = "".join(sampleMachine().graphviz())
        self.assertIn("begin", gvout)
        self.assertIn("end", gvout)
        self.assertIn("go", gvout)
        self.assertIn("out", gvout)
