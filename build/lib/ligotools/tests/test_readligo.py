from ligotools import readligo as rl
import numpy as np

def test_dq_channel_to_seglist():
    assert (len(rl.dq_channel_to_seglist(np.array([1,1,1,1])))==1)