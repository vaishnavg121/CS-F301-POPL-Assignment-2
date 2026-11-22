% P2 implementation unit: expression/3.
% expression(+Numbers, -Tree, -IntegerValue) enumerates every ordered
% binary expression tree using exactly Numbers as its leaves.
% Tree uses num(N) for leaves and op(Operator, Left, Right) for nodes.
% This unit constructs and evaluates trees; formatting and equations are
% separate predicates developed in later units.

expression([N], num(N), N) :-
    integer(N),
    N >= 0.

expression(Numbers, Tree, Value) :-
    append(LeftNumbers, RightNumbers, Numbers),
    LeftNumbers = [_|_],
    RightNumbers = [_|_],
    expression(LeftNumbers, LeftTree, LeftValue),
    expression(RightNumbers, RightTree, RightValue),
    (   Tree = op('+', LeftTree, RightTree),
        Value is LeftValue + RightValue
    ;   Tree = op('-', LeftTree, RightTree),
        Value is LeftValue - RightValue
    ;   Tree = op('*', LeftTree, RightTree),
        Value is LeftValue * RightValue
    ;   RightValue =\= 0,
        0 is LeftValue mod RightValue,
        Tree = op('/', LeftTree, RightTree),
        Value is LeftValue // RightValue
    ).
