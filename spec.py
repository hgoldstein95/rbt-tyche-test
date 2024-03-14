from hypothesis import Phase, given, settings, strategies as st, assume, event
from impl import *


def size(t: Tree) -> int:
    if isinstance(t, E):
        return 0
    elif isinstance(t, T):
        return 1 + size(t.l) + size(t.r)
    else:
        raise Exception("impossible")


def black_height(t: Tree) -> int:
    if isinstance(t, E):
        return 0
    elif isinstance(t, T):
        return (1 if t.c.is_black() else 0) + max(black_height(t.l),
                                                  black_height(t.r))
    else:
        raise Exception("impossible")


@st.composite
def trees(draw, max_depth=5):
    if max_depth == 0:
        return E()
    else:
        if not draw(st.booleans()):
            return E()
        return T(draw(st.one_of(st.just(Red()), st.just(Black()))),
                 draw(trees(max_depth - 1)), draw(st.integers()),
                 draw(st.integers()), draw(trees(max_depth - 1)))


@given(trees(), st.integers(), st.integers())
@settings(max_examples=100, phases=[Phase.generate])
def test_insert_valid(t: Tree, k: int, v: int):
    event("size", payload=size(t))
    event("black_height", payload=black_height(t))
    assume(is_rbt(t))
    assert is_rbt(insert(k, v, t))


@given(trees(), st.integers(), st.integers())
@settings(max_examples=100, phases=[Phase.generate])
def test_insert_lookup(t: Tree, k: int, v: int):
    event("size", payload=size(t))
    event("black_height", payload=black_height(t))
    assume(is_rbt(t))
    assert lookup(insert(k, v, t), k) == v


@given(trees(), st.integers())
@settings(max_examples=100, phases=[Phase.generate])
def test_delete_valid(t: Tree, k: int):
    event("size", payload=size(t))
    event("black_height", payload=black_height(t))
    assume(is_rbt(t))
    assert is_rbt(delete(k, t))


@given(trees(), st.integers())
@settings(max_examples=100, phases=[Phase.generate])
def test_delete_lookup(t: Tree, k: int):
    event("size", payload=size(t))
    event("black_height", payload=black_height(t))
    assume(is_rbt(t))
    assert lookup(delete(k, t), k) == None
