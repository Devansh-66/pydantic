import pytest
from pydantic import BaseModel


def test_nested_mutable_default_isolated():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child = Child()

    p1 = Parent()
    p2 = Parent()

    p1.child.items.append(1)

    assert p2.child.items == [], "Mutable defaults should not be shared across instances"


def test_multiple_levels_of_nesting():
    class Inner(BaseModel):
        values: dict[str, int] = {}

    class Middle(BaseModel):
        inner: Inner = Inner()

    class Outer(BaseModel):
        middle: Middle = Middle()

    o1 = Outer()
    o2 = Outer()

    o1.middle.inner.values["x"] = 10

    assert o2.middle.inner.values == {}, "Deep nested mutable defaults must be isolated"


def test_mutation_after_validation():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child

    p1 = Parent(child=Child())
    p2 = Parent(child=Child())

    p1.child.items.append(42)

    assert p2.child.items == [], "Explicit instances should also remain isolated"


def test_dict_and_list_combination():
    class Child(BaseModel):
        data: dict[str, list[int]] = {}

    class Parent(BaseModel):
        child: Child = Child()

    p1 = Parent()
    p2 = Parent()

    p1.child.data.setdefault("a", []).append(1)

    assert p2.child.data == {}, "Nested dict/list structures must not be shared"


def test_default_factory_equivalence():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child = Child()

    p1 = Parent()
    p2 = Parent()

    assert p1.child is not p2.child, "Each nested model should be a new instance"
