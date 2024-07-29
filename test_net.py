import pytest

from net import unit_definiton, split_by_layers

test_u = "  1 |          |          |  0.00000 |  0.00000 | i  |  2, 2, 0 |||"


class Test_unit_definition: 
    def test_constructor(self):
        new_unit = unit_definiton(1,"i","2, 2, 0") 
        assert new_unit == test_u

class Test_split:
    def test_split(self):
        assert split_by_layers(1,[1],1) == [[1],[2],[3]]
        assert split_by_layers(1,[1,1],1) == [[1],[2],[3],[4]]
        assert split_by_layers(1,[2],1) == [[1],[2,3],[4]]
