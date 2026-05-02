from pydantic import BaseModel, Field


def test_default_factory_isolation():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child = Field(default_factory=Child)

    p1 = Parent()
    p2 = Parent()

    p1.child.items.append(1)

    assert p2.child.items == []

def test_model_dump_roundtrip_isolation():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child = Field(default_factory=Child)

    p1 = Parent()
    data = p1.model_dump()
    p2 = Parent.model_validate(data)

    p1.child.items.append(7)

    assert p2.child.items == []
    
def test_model_copy_deep_copy():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child = Field(default_factory=Child)

    p1 = Parent()
    p2 = p1.model_copy()

    p1.child.items.append(10)

    assert p2.child.items == []


def test_model_validate_isolation():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child

    p1 = Parent.model_validate({"child": {}})
    p2 = Parent.model_validate({"child": {}})

    p1.child.items.append(5)

    assert p2.child.items == []


def test_deep_nested_structures():
    class Inner(BaseModel):
        values: dict[str, list[int]] = {}

    class Middle(BaseModel):
        inner: Inner = Field(default_factory=Inner)

    class Outer(BaseModel):
        middle: Middle = Field(default_factory=Middle)

    o1 = Outer()
    o2 = Outer()

    o1.middle.inner.values.setdefault("a", []).append(1)

    assert o2.middle.inner.values == {}


def test_copy_then_mutate_then_validate():
    class Child(BaseModel):
        items: list[int] = []

    class Parent(BaseModel):
        child: Child = Field(default_factory=Child)

    p1 = Parent()
    p2 = p1.model_copy()

    p1.child.items.append(99)

    p3 = Parent.model_validate(p2.model_dump())

    assert p2.child.items == []
    assert p3.child.items == []
